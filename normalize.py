from pydub import AudioSegment
from pydub.effects import normalize
import argparse
import os
import sys
import subprocess


def normalize_file(input_path, output_path=None, use_normalize=True, gain_db=0):
	if not os.path.isfile(input_path):
		raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

	audio = AudioSegment.from_file(input_path)

	if use_normalize:
		processed = normalize(audio)
	else:
		processed = audio + gain_db

	if not output_path:
		base = os.path.splitext(os.path.basename(input_path))[0]
		output_path = f"{base}_normalized.mp3"

	processed.export(output_path, format="mp3")
	return output_path


def ffmpeg_loudness_normalize(input_path, output_path, target_lufs=-14.0, true_peak=-1.5, lra=11):
	# Uses ffmpeg loudnorm filter for EBU R128 normalization
	af = f"loudnorm=I={target_lufs}:TP={true_peak}:LRA={lra}"
	cmd = [
		"ffmpeg",
		"-hide_banner",
		"-loglevel",
		"error",
		"-y",
		"-i",
		input_path,
		"-af",
		af,
		"-b:a",
		"192k",
		output_path,
	]
	subprocess.run(cmd, check=True)
	return output_path


def main():
	parser = argparse.ArgumentParser(description="Normaliza ou aumenta volume de um arquivo de áudio")
	parser.add_argument("-i", "--input", help="Caminho do arquivo de entrada")
	parser.add_argument("-d", "--input-dir", help="Caminho de uma pasta contendo arquivos de áudio para processar em lote")
	parser.add_argument("-o", "--output", help="Arquivo de saída (padrão: <input>_normalized.mp3) ou diretório quando usar --input-dir")
	parser.add_argument("-e", "--exts", help="Extensões a processar (separadas por vírgula), ex: mp3,wav", default="mp3")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--gain", type=int, help="Aumentar volume em dB (ex.: 10)")
	group.add_argument("--normalize", action="store_true", help="Normalizar o áudio (padrão)")
	parser.add_argument("--loudness", type=float, help="Aplicar normalização EBU R128 via ffmpeg loudnorm (valor LUFS, ex: -14)")
	args = parser.parse_args()
	use_normalize = args.normalize or (args.gain is None)

	# Batch directory processing
	if args.input_dir:
		input_dir = args.input_dir
		if not os.path.isdir(input_dir):
			print(f"Diretório não encontrado: {input_dir}", file=sys.stderr)
			sys.exit(1)

		exts = [e.strip().lstrip('.') for e in (args.exts or 'mp3').split(',')]
		out_dir = args.output or input_dir
		os.makedirs(out_dir, exist_ok=True)

		processed = 0
		out_dir_abs = os.path.abspath(out_dir)
		for root, dirs, files in os.walk(input_dir):
			# don't descend into the output directory if it's inside the input directory
			dirs[:] = [d for d in dirs if not os.path.abspath(os.path.join(root, d)).startswith(out_dir_abs)]
			for fname in files:
				# skip files that are already normalized to avoid repeated processing
				if fname.lower().endswith('_normalized.mp3'):
					continue
				if any(fname.lower().endswith('.' + ex) for ex in exts):
					in_path = os.path.join(root, fname)
					base = os.path.splitext(fname)[0]
					out_name = f"{base}_normalized.mp3"
					out_path = os.path.join(out_dir, out_name)
					try:
						if args.loudness is not None:
							ffmpeg_loudness_normalize(in_path, out_path, target_lufs=args.loudness)
						else:
							normalize_file(in_path, out_path, use_normalize=use_normalize, gain_db=(args.gain or 0))
						print(f"Processado: {in_path} -> {out_path}")
						processed += 1
					except Exception as e:
						print(f"Erro ao processar {in_path}: {e}", file=sys.stderr)

		print(f"Concluído. Arquivos processados: {processed}")
		sys.exit(0)

	# Single file processing
	if not args.input:
		print("Informe --input para um arquivo ou --input-dir para processar uma pasta.", file=sys.stderr)
		sys.exit(1)

	try:
		if args.loudness is not None:
			out_path = args.output or (os.path.splitext(os.path.basename(args.input))[0] + "_normalized.mp3")
			out = ffmpeg_loudness_normalize(args.input, out_path, target_lufs=args.loudness)
		else:
			out = normalize_file(args.input, args.output, use_normalize=use_normalize, gain_db=(args.gain or 0))
		print(f"Áudio salvo como: {out}")
	except Exception as e:
		print(f"Erro: {e}", file=sys.stderr)
		sys.exit(1)


if __name__ == "__main__":
	main()
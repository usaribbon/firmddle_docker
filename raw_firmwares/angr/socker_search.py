import angr
import monkeyhex
import os
import magic
import warnings
import sys
from datetime import datetime
from tqdm import tqdm

# Suppress warnings
warnings.filterwarnings("ignore")

def find_str_symbol_references(binary_path, log_file):
    try:
        project = angr.Project(binary_path, auto_load_libs=False)
        cfg = project.analyses.CFG(normalize=True, data_references=True)
        symbols = project.loader.main_object.symbols
        str_symbols = [sym for sym in symbols if 'str' in sym.name.lower()]
        
        for sym in str_symbols:
            print(f"Symbol: {sym.name}", file=log_file)
            print("Referenced by functions:", file=log_file)
            sym_addr = sym.rebased_addr
            for func in cfg.functions.values():
                for block in func.blocks:
                    for insn in block.capstone.insns:
                        if sym_addr in insn.operands:
                            print(f"  Function: {func.name}", file=log_file)
                            print("  Pseudocode:", file=log_file)
                            print(func, file=log_file)
                            try:
                                decompilation = project.analyses.Decompiler(func, cfg=cfg)
                                print(decompilation, file=log_file)
                                if decompilation.codegen is not None:
                                    print(decompilation.codegen.text, file=log_file)
                                else:
                                    print("    Unable to generate pseudocode for this function.", file=log_file)
                            except Exception as e:
                                print(f"    Error during decompilation: {type(e).__name__}: {str(e)}", file=log_file)
                            print(file=log_file)
                            break
            print(file=log_file)
    except Exception as e:
        print(f"Error analyzing {binary_path}: {type(e).__name__}: {str(e)}", file=log_file)

def is_elf_file(file_path):
    return 'ELF' in magic.from_file(file_path)

def analyze_firmware(firmware_dir, log_dir):
    elf_files = []
    for root, dirs, files in os.walk(firmware_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_elf_file(file_path):
                elf_files.append(file_path)
    
    if not elf_files:
        print(f"No ELF files found in {firmware_dir}")
        return

    print(f"Found {len(elf_files)} ELF files in {firmware_dir}. Starting analysis...")
    
    # Create a log file for this firmware
    log_filename = os.path.join(log_dir, f"elf_analysis_log_{os.path.basename(firmware_dir)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(log_filename, "w", encoding="utf-8") as log_file:
        print(f"Analyzing firmware: {firmware_dir}", file=log_file)
        print(f"Number of ELF files: {len(elf_files)}", file=log_file)
        print("-" * 50, file=log_file)
        
        for file_path in tqdm(elf_files, desc=f"Analyzing ELF files in {firmware_dir}"):
            print(f"\nAnalyzing: {file_path}", file=log_file)
            find_str_symbol_references(file_path, log_file)
            print("-" * 50, file=log_file)
    
    print(f"Analysis for {firmware_dir} complete. Log saved to {log_filename}")

if __name__ == "__main__":
    base_directory = "/mnt/raw_firmwares/extracted"
    log_directory = "logfile"
    
    # Create log directory if it doesn't exist
    os.makedirs(log_directory, exist_ok=True)
    
    # Analyze each firmware directory
    for firmware_dir in os.listdir(base_directory):
        firmware_path = os.path.join(base_directory, firmware_dir)
        if os.path.isdir(firmware_path):
            print(f"Analyzing firmware: {firmware_path}")
            analyze_firmware(firmware_path, log_directory)
    
    print("All firmware analyses complete.")

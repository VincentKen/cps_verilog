import json
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
import os

DATASET = "../dataset"

VERILOG_KEYWORDS = [
    "always", "and", "assign", "automatic", "begin", "buf", "bufif0", "bufif1", "case", "casex",
    "casez", "cell", "cmos", "config", "deassign", "default", "defparam", "design", "disable",
    "edge", "else", "end", "endcase", "endconfig", "endfunction", "endgenerate", "endmodule",
    "endprimitive", "endspecify", "endtable", "endtask", "event", "for", "force", "forever",
    "fork", "function", "generate", "genvar", "highz0", "highz1", "if", "ifnone", "incdir",
    "include", "initial", "inout", "input", "instance", "integer", "join", "large", "liblist",
    "library", "localparam", "macromodule", "medium", "module", "nand", "negedge", "nmos",
    "nor", "noshowcancelled", "not", "notif0", "notif1", "or", "output", "parameter", "pmos",
    "posedge", "primitive", "pull0", "pull1", "pulldown", "pullup", "rcmos", "real", "realtime",
    "reg", "release", "repeat", "rnmos", "rpmos", "rtran", "rtranif0", "rtranif1", "scalared",
    "showcancelled", "signed", "small", "specify", "specparam", "strong0", "strong1", "supply0",
    "supply1", "table", "task", "time", "tran", "tranif0", "tranif1", "tri", "tri0", "tri1",
    "triand", "trior", "trireg", "unsigned", "use", "uwire", "vectored", "wait", "wand", "weak0",
    "weak1", "while", "wire", "wor", "xnor", "xor"
]

def generate_training_data_file_list(path=DATASET):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".v") and not file.endswith("tb.v"):
                file_list.append(os.path.join(root, file))
    return file_list


def train_tokenizer():
    verilog_tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[MASK]"] + VERILOG_KEYWORDS)
    verilog_tokenizer.train(generate_training_data_file_list(), trainer)
    verilog_tokenizer.save("verilog_tokenizer.json")

def get_tokenizer():
    try:
        return Tokenizer.from_file("verilog_tokenizer.json")
    except:
        train_tokenizer()
        return Tokenizer.from_file("verilog_tokenizer.json")

verilog_tokenizer = get_tokenizer()
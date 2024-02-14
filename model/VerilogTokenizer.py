import json
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import os
import sys

DATASET = "../dataset"
DATASET = os.path.join(os.path.dirname(__file__), DATASET)
TOKENIZER = "verilog_tokenizer.json"
TOKENIZER = os.path.join(os.path.dirname(__file__), TOKENIZER)

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
    verilog_tokenizer.pre_tokenizer = Whitespace()
    trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[MASK]"] + VERILOG_KEYWORDS)
    verilog_tokenizer.train(generate_training_data_file_list(), trainer)
    verilog_tokenizer.save(TOKENIZER)


def get_tokenizer(train=False):
    if train:
        train_tokenizer()
    try:
        return Tokenizer.from_file(TOKENIZER)
    except:
        print("Tokenizer not found")
        print("Tokenizer might require training (get_tokenizer(traint=True))")
        return None


if __name__ == "__main__":
    # check arguments for training requirement
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        verilog_tokenizer = get_tokenizer(train=True)
    else:
        verilog_tokenizer = get_tokenizer()
    print(verilog_tokenizer.encode("module test(input wire a, output wire b); endmodule").tokens)
    print(verilog_tokenizer.encode("module test(input wire a, output wire b); endmodule").ids)
    print(verilog_tokenizer.encode("module test(input wire a, output wire b); endmodule").attention_mask)
    print(verilog_tokenizer.encode("module test(input wire a, output wire b); endmodule").offsets)
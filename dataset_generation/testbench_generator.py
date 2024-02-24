import hdlparse.verilog_parser as vlog
import re
import random
import sys

print('------------------- Verilog Testbench Generator -------------------')
vlog_ex = vlog.VerilogExtractor()
fname = sys.argv[1]
with open(fname, 'rt') as fh:
    code = fh.read()
vlog_mods = vlog_ex.extract_objects_from_source(code)

vlog_mods = vlog_ex.extract_objects(fname)


def vector_size(line):
    if re.search(r'\[', line):
        lval = re.findall(r'\[(.*):', line)[0]
        rval = re.findall(r'\[.*:(.*)\]', line)[0]
        return (abs(int(rval) - int(lval)) + 1)
    return 1


for m in vlog_mods:
    print('Module "{}":'.format(m.name))
    inputs_list = []
    print('\n  Ports:')
    for p in m.ports:
        if (p.data_type).find('[') != -1:
            inputs_list.append({"name": p.name, "mode": p.mode, "data_type": (p.data_type).split()[0],
                                "length": vector_size((p.data_type).split()[1])})
        else:
            inputs_list.append({"name": p.name, "mode": p.mode, "data_type": p.data_type, "length": 1})
        print('\t{:20}{:8}{}'.format(p.name, p.mode, p.data_type))

if_cases_conditions = set()
always_conditions = set()
case_conditions = set()


def parse_if(line):
    if line.find("||") != -1 or line.find("&&") != -1:
        for port in inputs_list:
            if port["mode"] == "input":
                if line.find(port["name"]) != -1:
                    if_cases_conditions.add(port["name"])
    else:
        s = re.split(r"if\s*\(\s*!?", line)[1]
        s = re.split(r"\s*\)", s)[0]
        if_cases_conditions.add(s)


def parse_always(line):
    if line.find("||") != -1 or line.find("&&") != -1 or line.find("or") != -1 or line.find("and") != -1:
        for port in inputs_list:
            if port["mode"] == "input":
                if line.find(port["name"]) != -1:
                    always_conditions.add(port["name"])
    else:
        s = re.split(r"always\s*@\s*\(\s*!?", line)[1]
        s = re.split(r"\s*\)", s)[0]
        always_conditions.add(s)


def parse_case(line):
    s = re.split(r"case\s*\(\s*", line)[1]
    s = re.split(r"\s*\)", s)[0]
    case_conditions.add(s)


file = open(fname, "rt")
for line in file:
    if re.search(r"if\s*\(\s*\w+", line):
        parse_if(line)
    if re.search(r"always\s*@\s*\(\s*\w+\s*", line):
        parse_always(line)
    if re.search(r"case\s*\(\s*\w+\s*\)", line):
        parse_case(line)


# print(if_cases_conditions)
# print(always_conditions)
# print(case_conditions)


def generate_range(port_length):
    if port_length == 1:
        return '1'
    else:
        return str(pow(2, port_length) - 1)


def generate_vector(port_length):
    if port_length == 1:
        return ' '
    else:
        return (' [' + str(port_length - 1) + ':0] ')


def testbench_header_and_ports():
    content = ""
    content += ('module testbench();\n')
    for port in inputs_list:
        if port["mode"].find('input', 0, 5) != -1:
            content += ('    ' + port["mode"].replace('input', 'reg') + generate_vector(port["length"]) + port[
                "name"] + '_tb;\n')
        elif port["mode"].find('output', 0, 6) != -1:
            content += ('    ' + port["mode"].replace('output', 'wire') + generate_vector(port["length"]) + port[
                "name"] + '_tb;\n')
    return content


def testbench_initial_block(time_delay):
    global val
    content = ""
    content += ('  integer i;\n  begin\n//initial block\ninitial\n  begin\n    //initial values\n')
    minPortSize = 5
    for port in inputs_list:
        minPortSize = max(port["length"], minPortSize)
    iterationCounter = int(pow(2, minPortSize) / 2)
    iterationCounter = min(iterationCounter, 30)
    for i in range(iterationCounter):
        if (i != 0):
            content += ('  #' + str(time_delay) + '\n')
        for line in inputs_list:
            if line["mode"] == 'input':
                val = line["length"]
                content += ('    ' + line["name"] + '_tb = ' + str(val) + '\'b' + bin(
                    random.randint(0, pow(2, val) - 1))[2:].zfill(val) + ';' + '\n')

    content += ('\n//Random generated constraints\n')
    content += ('for(i = 0; i < 100; i = i+1)\n  begin\n  #' + str(time_delay) + '\n')
    for line in inputs_list:
        if line["mode"] == 'input':
            val = line["length"]
            content += ('    ' + line["name"] + '_tb = ' + '$urandom_range(0,' + generate_range(val) + ');' + '\n')
    content += ('  end\n')
    content += ('  $finish;\nend\n')
    return content


def testbench_design_instance():
    content = ""
    content += ('// instaniate design instance\n  ' + m.name + ' DUT (\n')
    for i, line in enumerate(inputs_list, 0):
        content += ('    .' + (line["name"]).replace('_tb', '') + '(' + line["name"] + '_tb' + ')')
        if i != len(inputs_list) - 1:
            content += (',\n')
        else:
            content += ('\n);\n')
    return content


def testbench_monitor_block():
    content = ""
    word_size = []
    content += ('initial begin\n  $display ("        			","Time ')
    for port in inputs_list:
        content += (port["name"] + '  ')
        word_size.append(len(port["name"]))
    content += ('");\n  $monitor ("     %d')
    for i in range(1, len(inputs_list) + 1):
        w = max(word_size[i - 1], port["length"])
        content += ('{space:{width}}{id}'.format(space=' ', width=w, id='%d'))
    content += ('" , $time')
    for port in inputs_list:
        content += (',' + port["name"] + '_tb')
    content += (');\nend\nend\nendmodule')
    return content


def generate_output_file(file_content):
    output_file = fname.replace('.v', '_tb.v')
    if len(file_content) == 0:
        return
    with open(output_file, 'w') as f:
        f.write(file_content)


time_delay = 10
test_bench_content = ""
test_bench_content += testbench_header_and_ports() + testbench_initial_block(
    time_delay) + testbench_design_instance() + testbench_monitor_block()

generate_output_file(test_bench_content)


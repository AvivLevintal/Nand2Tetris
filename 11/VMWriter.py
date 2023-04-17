class VMWriter():

    output_file = None
    def __init__(self, output_file):
        self.output_file = open(output_file, 'w')
        
    def write_push(self,segment, index):
        self.output_file.write('push {} {}\n'.format(segment, index))


    def write_pop(self,segment, index):
        self.output_file.write('pop {} {}\n'.format(segment, index))


    def write_arithmetic(self,command):
        self.output_file.write('{}\n'.format(command))


    def write_label(self,label):
        self.output_file.write('label {}\n'.format(label))


    def write_goto(self,label):
        self.output_file.write('goto {}\n'.format(label))


    def write_if(self,label):
        self.output_file.write('if-goto {}\n'.format(label))


    def write_call(self,name, num_args):
        self.output_file.write('call {} {}\n'.format(name, num_args))


    def write_function(self,name, num_locals):
        self.output_file.write('function {} {}\n'.format(name, num_locals))


    def write_return(self):
        self.output_file.write('return\n')

    def close(self):
        self.output_file.close()
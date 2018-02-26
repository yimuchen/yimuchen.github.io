#!/bin/env python
#-------------------------------------------------------------------------------
#
#  Filename    : update_mathjax.py
#  Description : updating the mathjax.html from when given a new .sty file
#  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
#
#-------------------------------------------------------------------------------
import re
import argparse
import pprint

parser = argparse.ArgumentParser(prog='update_mathjax',
    description='updating the existing mathjax.html file to include macros from other files'
)

parser.add_argument(
    '-i', '--inputfile', required=True,
    type=argparse.FileType('r'),
    help='Input .sty file to look for new commands'
)

#-------------------------------------------------------------------------------
#   Main control flows
#-------------------------------------------------------------------------------
def main():
    args = parser.parse_args()
    newmacro = get_newmacro( args.inputfile )
    oldmacro = get_oldmacro()
    print(oldmacro)
    mergemacro = merge_macro( oldmacro, newmacro, args )
    makehtml( mergemacro )

def get_newmacro( sty_file ):
    cmdlist = []
    argcmd = re.compile(r'\\newcommand\{\\(\w+)\}\[(\d)+\]\{(.*)\}')
    symcmd = re.compile(r'\\newcommand\{\\(\w+)\}\{(.*)\}')
    ensure = re.compile(r'\\ensuremath\{(.*)\}')

    def reform( cmd ):
        if( ensure.match(cmd) ): # removing \\ensuremath command
            cmd =  ensure.match(cmd)[1]
        cmd = re.sub(r'\\',r'\\\\',cmd)
        cmd = re.sub(r"'",r"\'",cmd)
        cmd = re.sub(r"\\text\{","\\mathrm{",cmd)
        return cmd

    def make_numcmd( cmd , num ):
        cmd = reform(cmd)
        return "[\'{}\',{}]".format(cmd,num)

    def make_cmd(cmd):
        cmd = reform(cmd)
        return "'{}'".format(cmd)

    for line in sty_file.readlines():
        argmatch = argcmd.match( line )
        symmatch = symcmd.match( line )
        if argmatch :
            cmdlist.append({
                'name': argmatch[1],
                'cmd': make_numcmd(argmatch[3],argmatch[2])
                })
        elif symmatch :
            cmdlist.append({
                'name':symmatch[1],
                'cmd':make_cmd(symmatch[2])
            })
    return cmdlist

def get_oldmacro():
    cmdlist = []
    beginpat = re.compile(r'\s*Macros:\s*\{\s*')
    endpat   = re.compile(r'\s*\}\s*')
    cmdpat   = re.compile(r'\s*(\w+):\s*(.*)\s*,\s*')

    with open('mathjax.html','r') as mathjax:
        begin = False
        for line in mathjax.readlines():
            if begin and endpat.match(line):
                break

            cmdmatch = cmdpat.match(line.strip())
            if begin and cmdmatch:
                cmdlist.append({
                    'name':cmdmatch[1],
                    'cmd':cmdmatch[2]
                })

            if beginpat.match(line):
                begin = True
    return cmdlist

def merge_macro( oldmacro, newmacro, args ):
    macrolist = [x for x in oldmacro]
    for new in newmacro :
        macrodict = [x['name'] for x in macrolist ]
        if new['name'] in macrodict:
            print("Updating! {}".format(new['name']))
            for x in macrolist :
                if x['name'] == new['name']:
                    x['cmd'] = new['cmd']
        else:
            macrolist.append( new )
            print("New entry! {}".format(new['name']))
    return macrolist

def makehtml( mergemacro ):
    cmdstrlist = ["     {}:{}".format(x['name'],x['cmd']) for x in mergemacro ]
    cmdstr = ',\n'.join(cmdstrlist)
    content = """
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
MathJax.Hub.Config({{
  tex2jax: {{
    inlineMath: [['$','$']],
    processEscapes: true
  }},
  TeX: {{
    Macros: {{
{}
    }}
  }}
}});
</script>
""".format(cmdstr)

    with open('mathjax.html','w') as mathjax:
        mathjax.write(content)

if __name__ == '__main__':
    main()

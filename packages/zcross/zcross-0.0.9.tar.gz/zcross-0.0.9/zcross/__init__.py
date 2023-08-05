import xml.etree.ElementTree as et

import re
import os
import inspect

from zcross.raw.binding import *
import zcross.raw.binding as raw_binding

import pyxb.utils.domutils
pyxb.utils.domutils.BindingDOMSupport.SetDefaultNamespace("https://zcross.net")

re_reference   = re.compile(r'@(\w+){([\w\-]+),([\s\S]*)}', re.MULTILINE)
re_whitespace  = re.compile(r'\s+', re.MULTILINE)
re_database_id = re.compile(r'\<database\s+id\s*=\s*\"([A-Za-z0-9]+)\"', re.MULTILINE)

def load_by_xml(filename):
    with open(filename, 'r') as f:
        return raw_binding.CreateFromDocument(f.read())
    
def save_to_xml(document, filename):
    
    with open(filename, 'w') as f:
        f.write(document.toxml("utf-8", element_name='zcross').decode('utf-8'))

def _get_data_dir():
    data_dir = None
    
    if 'ZCROSS_DATA' in os.environ and os.path.exists(os.environ['ZCROSS_DATA']):
        data_dir = os.environ['ZCROSS_DATA']  
    elif os.path.exists('/opt/zcross_data'):
        data_dir = '/opt/zcross_data'
        
    if data_dir is None:
        raise Exception('Unable to find ZCross data file: define ZCROSS_DATA env variable.')
      
    return data_dir
    
def load_by_name(database):
  
    for r, d, f in os.walk(_get_data_dir()):
        for fx in f:
            if fx.endswith('.xml'):
                filename = os.path.join(r, fx)
                with open(filename, 'r') as f:
                    header = f.read(1024) # reading the first caracters of the XML files whitout loading everything in memory
                    m = re_database_id.search(header)
                    if m and m.group(1).lower() == database.lower():
                        f.seek(0)
                        return raw_binding.CreateFromDocument(f.read())
    
def load_all(verbose = False):
  
    contents = []
   
    for r, d, f in os.walk(_get_data_dir()):
        for fx in f:
            if fx.endswith('.xml'):
                filename = os.path.join(r, fx)

                with open(filename, 'r') as f:
                    if verbose:
                        print('Loading {}'.format(filename))
                    contents.append(raw_binding.CreateFromDocument(f.read()))
    return contents
                    

    
class ZCross(raw_binding.ZCross):
    pass
    
class Reference(raw_binding.Reference):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        m = re_reference.match(self.value())
        
        if m:
            self.label = m.group(2)
            self.type = m.group(1)
            content = m.group(3)
            
            # Parsing content
            
            section = 0
            
            current_key = ''
            current_value = ''
                        
             
            level = 0
                     
            for c in content:

                if c == '=' and level == 0:
                    if section == 0:
                        section = 1
                        continue
                elif c == ',' and level == 0:
                    if section == 1:
                        section = 2
                        continue
                elif c == '{':
                    level += 1
                elif c == '}':
                    level -= 1
                    
                
                if section == 0:
                    current_key += c
                if section == 1:
                    current_value += c
                if section == 2:
                    key = current_key.strip()
                    value = current_value.strip()
                    
                    if value.startswith('{') and value.endswith('}'):
                        value = value.strip('{').strip('}')
                        
                    setattr(self, key, value)
                    
                    current_key   = ''
                    current_value = ''
                    level = 0
                    section = 0
       
    def bibtex(self):
        s = '@{}{{{},\n'.format(self.type, self.label)
        for k,v in vars(self).items():
            if k not in ['label','type','id']:
                s += '\t{} = {{{}}},\n'.format(k,v)
        s += '}'
        
        return s
        
      
class Process(raw_binding.Process):
    
    def __str__(self):
        s = ''      
        s += ' + '.join(str(r.value) for r in self.reactants.orderedContent())
        s += ' → '
        s += ' + '.join(str(p.value) for p in self.products.orderedContent())
        return s
        
  
    def get_simple_type(self):
        if self.collisionType == 'elastic':
            if self.momentOrder == 0:
                return  'ela el'
            elif self.momentOrder == 1:
                return  'ela mt'
            elif self.momentOrder == 2:
                return  'ela vs'
            else:
                return  'ela {}'.format(self.moment_order)
        elif self.collisionType == 'inelastic':
            if   self.inelasticType == 'excitation_ele':
                return  'exc ele' + (' (' + self.products[0].molecule[0].state + ')') if len(self.products) and len(self.products[0].molecule) and self.products[0].molecule[0].state is not None else ''
            elif self.inelasticType == 'excitation_vib':
                return  'exc vib' + (' (' + self.products[0].molecule[0].state + ')') if len(self.products) and len(self.products[0].molecule) and self.products[0].molecule[0].state is not None else ''
            elif self.inelasticType == 'excitation_rot':
                return  'exc rot' + (' (' + self.products[0].molecule[0].state + ')') if len(self.products) and len(self.products[0].molecule) and self.products[0].molecule[0].state is not None else ''
            elif self.inelasticType == 'ionization':
                return  'ion' + (' ' + str(self.products[0].molecule[0])) if len(self.products) and len(self.products[0].molecule) else ''
            elif self.inelasticType == 'attachment':
                return  'att' + (' ' + str(self.products[0].molecule[0])) if len(self.products) and len(self.products[0].molecule) else ''
            elif self.inelasticType == 'neutral':
                return  'neu'
            else:
                return  '???'
        else:
            return  '???'
   
        
class Electron(raw_binding.Electron):

    def __str__(self):
        return 'e'
        
        
molecule_pat1 = re.compile('([0-9]+)')
molecule_pat2 = re.compile('\s*([A-Z][a-z]?)([0-9]*)\s*')

class Molecule(raw_binding.Molecule):
        
    def __str__(self):
        
        s = self.orderedContent()[0].value
        
        if self.charge != None:
            if abs(self.charge) > 1:
                s += (get_scripted_number(abs(self.charge), True, False) if abs(self.charge) >  1 else '') 
                
            if self.charge > 0:
                s += '⁺'
                
            if self.charge < 0:
                s += '⁻'
                
        if self.state != None:
            s += '(' + self.state + ')'
        
        return s
        
        
    # def explode(self):
        
        # s = self.value
        # global_reciept = {}

        # for start,end,level in self.__find_parens():

            # local_reciept = {}
            
            # formula  = s[start+1:end]
            # multiply = 1 
            # m1 = molecule_pat1.match(s, end+1)
            # if m1:
                # multiply = int(m1.group(1))
                # end = m1.span(1)[1]
                
            # # Parsing   
            # m2 = molecule_pat2.match(formula)
            # while m2:
                # atom = m2.group(1)
                
                # qty  = 1
                # if m2.group(2):
                    # qty = int(m2.group(2))
                    
                # if atom not in local_reciept:
                    # local_reciept[atom] = 0
                # local_reciept[atom] += qty
                                
                # m2 = molecule_pat2.match(formula, m2.span(1)[1])
                
            
            # for atom, qty in local_reciept.items():
                
                # if atom not in global_reciept:
                    # global_reciept[atom] = 0
                
                # global_reciept[atom] += qty * multiply
                
            # # Cleaning
            # s = s[:start] + ' ' * (end-start+1) + s[end+1:]
                
        # return global_reciept
                 
            
            
        
    # def __find_parens(self):
        # results = []
        # pstack = []
        
        # results.append((-1, len(self.value), 0))

        # for i, c in enumerate(self.value):
            # if c == '(':
                # pstack.append(i)
            # elif c == ')':
                # if len(pstack) == 0:
                    # raise IndexError("No matching closing parens at: " + str(i))
                # results.append((pstack.pop(), i, len(pstack)+1))

        # if len(pstack) > 0:
            # raise IndexError("No matching opening parens at: " + str(pstack.pop()))

        # results.sort(key=lambda result: result[0], reverse=True)
        
        # return results
    
    
class Parameter(raw_binding.Parameter):
    def __str__(self):
        return self.name + ' = ' + self.value + (' ' + self.units if hasattr(self, 'units') else '')
    
   
    
    
def get_scripted_number(number, superscript, forcePlus):

    if not isinstance(number, int):
        raise "Argument 'number' must be an int"

    digitsSuper = ['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹']
    digitsSub   = ['₀','₁','₂','₃','₄','₅','₆','₇','₈','₉']

    s= ''

    if number < 0:
        if superscript:
            s += '⁻';
        else:
            s += '₋';
    
    elif number > 0 and forcePlus:
        if superscript:
            s += '⁺'
        else:
            s += '₊'

    while number > 0:
        
        if superscript:
            s = digitsSuper[number % 10] + s
        else:
            s = digitsSub[number % 10] + s
            
        number //= 10
    

    return s




raw_binding.ZCross._SetSupersedingClass(ZCross)
raw_binding.Electron._SetSupersedingClass(Electron)
raw_binding.Molecule._SetSupersedingClass(Molecule)
raw_binding.Parameter._SetSupersedingClass(Parameter)
raw_binding.Process._SetSupersedingClass(Process)
raw_binding.Reference._SetSupersedingClass(Reference)





# Utility function to identify classes of interest
def _isSupersedable (cls):
    return inspect.isclass(cls) and issubclass(cls, pyxb.binding.basis._DynamicCreate_mixin)

def _injectClasses ():
    import sys
    import pyxb.binding.basis

    # All PyXB complex type definitions in the original module
    raw_classes = set([_o for (_, _o) in inspect.getmembers(raw_binding) if _isSupersedable(_o)])
    #print 'Original classes: %s' % (raw_classes,)

    # PyXB complex type definitions in this module that did not come
    # from the original import *.
    this_module = sys.modules[__name__]
    this_classes = set([_o for (_, _o) in inspect.getmembers(this_module) if _isSupersedable(_o) and _o not in raw_classes])
    this_classes_tuple = tuple(this_classes)
    #print 'This classes: %s' % (this_classes,)

    # Raw classes superseded by something in this module
    superseded_classes = set([ _o for _o in raw_classes if _o._SupersedingClass() in this_classes ])
    superseded_classes_tuple = tuple(superseded_classes)
    #print 'Superseded classes: %s' % (superseded_classes,)

    # Raw classes that are subclasses of something superseded by this
    # module, but that are not themselves superseded by this module
    need_supersedure_classes = set([_o for _o in raw_classes if issubclass(_o, superseded_classes_tuple) and _o not in superseded_classes])
    #print 'Need supersedure classes: %s' % (need_supersedure_classes,)

    # Add local definitions to supersede classes all of whose
    # ancestors have been superseded as necessary.
    while need_supersedure_classes:
        did_replacement = False
        new_need_supersedure_classes = set()
        for o in need_supersedure_classes:
            candidate = True
            # Build the new sequence of base classes while we check them.
            new_mro = []
            for super_o in o.__mro__:
                if super_o == o:
                    # Put the superseded class in its original position (probably first)
                    new_mro.append(o)
                    continue
                if super_o in need_supersedure_classes:
                    # Subclass of a class we haven't gotten to yet; put it off
                    candidate = False
                    break
                # Append the replacement or the original, as needed
                if super_o in superseded_classes:
                    new_mro.append(super_o._SupersedingClass())
                else:
                    new_mro.append(super_o)
            if not candidate:
                new_need_supersedure_classes.add(o)
                continue
            # Create a new class that subclasses the replacements
            name = o.__name__
            new_o = type(name, tuple(new_mro), o.__dict__.copy())
            # Install it in the module
            setattr(this_module, name, new_o)
            # Tell PyXB to use it as the superseding class
            o._SetSupersedingClass(new_o)
            # Record it so future passes will find it
            superseded_classes.add(o)
        assert need_supersedure_classes != new_need_supersedure_classes
        need_supersedure_classes = new_need_supersedure_classes

_injectClasses()


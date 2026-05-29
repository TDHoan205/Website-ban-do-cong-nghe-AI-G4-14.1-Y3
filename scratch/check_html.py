# -*- coding: utf-8 -*-
from pathlib import Path
import re

c = Path(r'd:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Home\index.html').read_text(encoding='utf-8')
# Check all tags are properly formed
bad_tags = 0
open_div = c.count('<div')
close_div = c.count('</div>')
open_section = c.count('<section')
close_section = c.count('</section>')
open_button = c.count('<button')
close_button = c.count('</button>')
open_a = c.count('<a ')
close_a = c.count('</a>')
open_span = c.count('<span')
close_span = c.count('</span>')
open_p = c.count('<p>')
close_p = c.count('</p>')

print(f'Div: {open_div} open, {close_div} close')
print(f'Section: {open_section} open, {close_section} close')
print(f'Button: {open_button} open, {close_button} close')
print(f'A: {open_a} open, {close_a} close')
print(f'Span: {open_span} open, {close_span} close')
print(f'P: {open_p} open, {close_p} close')
print(f'All balanced: {open_div==close_div and open_section==close_section and open_button==close_button}')

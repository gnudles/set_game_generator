#!/usr/bin/env python3                                                          

import random,math
import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg
import cairo
DEGREES = math.pi / 180.0
def draw_rounded(cr, x,y,width,height, radius):
    """ draws rectangles with rounded (circular arc) corners """
    cr.arc(x + width - radius, y + radius, radius, -90 * DEGREES, 0 * DEGREES)
    cr.arc(x + width - radius, y + height - radius, radius, 0 * DEGREES, 90 * DEGREES)
    cr.arc(x + radius, y + height - radius, radius, 90 * DEGREES, 180 * DEGREES)  # ;o)
    cr.arc(x + radius, y + radius, radius, 180 * DEGREES, 270 * DEGREES)
    cr.close_path()
def draw_diamond(cr, x, y, x_radius,y_radius):
    cr.move_to(x+x_radius, y)
    cr.line_to(x,y+y_radius)
    cr.line_to(x-x_radius,y)
    cr.line_to(x,y-y_radius)
    cr.close_path()
def draw_oval(cr, x, y, x_radius,y_radius):
    draw_rounded(cr, x-x_radius,y-y_radius,x_radius*2,y_radius*2, y_radius)
def draw_star(cr, x, y, x_radius,y_radius):
    cr.move_to(x+x_radius, y+y_radius)
    cr.line_to(x,y+y_radius/2)
    cr.line_to(x-x_radius,y+y_radius)
    cr.line_to(x-x_radius/2,y)
    cr.line_to(x-x_radius,y-y_radius)
    cr.line_to(x,y-y_radius/2)
    cr.line_to(x+x_radius,y-y_radius)
    
    cr.line_to(x+x_radius/2,y)
    cr.line_to(x+x_radius,y+y_radius)
    cr.close_path()
def draw_wiggle_curve(cr, x, y, x_radius,y_radius):
    r1 = 34
    r2 = 5
    r3 = 8
    cx1 = r2+r3
    cx3 = r1+r2
    cx2 = r1-r3
    cr.save()
    cr.translate(x,y)
    cr.scale(x_radius/(r1+r2+r3),y_radius/(r1))
    cr.move_to(-cx1, r1)
    cr.curve_to(-cx1+r1, r1, cx2-r2, -r2/2, cx2, -r2/2)
    cr.curve_to(cx2+r2, -r2/2, cx3-r3, r3, cx3, r3)
    cr.curve_to(cx3+r3, r3, cx1+r1, -r1, cx1, -r1)
    cr.curve_to(cx1-r1, -r1, -cx2+r2, r2/2, -cx2, r2/2)
    cr.curve_to(-cx2-r2, r2/2, -cx3+r3, -r3, -cx3, -r3)
    cr.curve_to(-cx3-r3, -r3, -cx1-r1, r1, -cx1, r1)
    cr.close_path()
    cr.restore()
def draw_wiggle(cr, x, y, x_radius,y_radius):
    r1 = 38
    r2 = 8
    r3 = 4
    cx1 = r2+r3
    cx3 = r1+r2
    cx2 = r1-r3
    cr.save()
    cr.translate(x,y)
    cr.scale(x_radius/(r1+r2+r3),y_radius/(r1))
    cr.move_to(cx1-r1,0)
    cr.arc(cx1, 0, r1, 180 * DEGREES, 0 * DEGREES)
    cr.arc(cx3, 0, r3, 0 * DEGREES, 180 * DEGREES)
    cr.move_to(cx2-r2,0)
    cr.arc(cx2, 0, r2, 180 * DEGREES, 0 * DEGREES)
    cr.move_to(cx2-r2,0)
    cr.arc(-cx1, 0, r1, 0 * DEGREES, 180 * DEGREES)
    cr.arc(-cx3, 0, r3, 180 * DEGREES, 0 * DEGREES)
    cr.move_to(-cx2+r2,0)
    cr.arc(-cx2, 0, r2, 0 * DEGREES, 180 * DEGREES)
    cr.move_to(cx1-r1,0)
    cr.close_path()
    cr.restore()
y_positions=[[0.5],[0.36,0.64],[0.22,0.5,0.78],[0.17,0.39,0.61,0.83]]
shapes = [draw_diamond,draw_oval,draw_wiggle_curve,draw_star]
shape_y_rad = [0.09,0.076,0.082,0.08]

colours = [[0x7d/255.0,0xed/255.0,0x05/255.0],[0x05/255.0,0xa2/255.0,0xed/255.0],[0xed/255.0,0x05/255.0,0x91/255.0],[0xed/255.0,0xb8/255.0,0x05/255.0]]#[[0.3,0.6,0.9],[0.9,0.2,0.2],[0.2,0.9,0.4]]
def stroke_normal(ctx,w,col):
    ctx.set_line_width(w)
    #ctx.set_dash([6.0, 5.0])
    ctx.stroke()
def stroke2(ctx,w,col):
    ctx.set_dash([1])
    ctx.set_line_width(w*0.8)
    ctx.set_source_rgb(1, 1, 1)
    ctx.stroke_preserve()
    ctx.set_source_rgb(col[0],col[1],col[2])
    ctx.set_line_width(w*0.6)
    ctx.stroke()
def stroke_dash(ctx,w,col):
    ctx.set_dash([1])
    ctx.set_line_width(w*0.5)
    ctx.set_source_rgb(1, 1, 1)
    ctx.stroke_preserve()
    ctx.set_source_rgb(col[0],col[1],col[2])
    ctx.set_line_width(w*0.4)
    ctx.set_dash([3.0, 3.0])
    ctx.stroke()
def stroke_two_lines(ctx,w,col):
    ctx.set_line_width(w)
    ctx.set_source_rgb(col[0],col[1],col[2])
    ctx.stroke_preserve()
    ctx.set_line_width(w*0.3)
    ctx.set_source_rgb(1, 1, 1)
    ctx.stroke()

strokes=[stroke_two_lines,stroke_dash,stroke2,stroke_normal]


def make_pattern_lines(col):
    pattern_surface = \
        cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, (0, 0, 32, 4))
    ctx = cairo.Context(pattern_surface)
    ctx.set_line_width(4)
    ctx.set_source_rgb(col[0],col[1],col[2])
    ctx.move_to(0, 0)
    ctx.line_to(32, 0)
    ctx.stroke()
    pattern = cairo.SurfacePattern(pattern_surface)
    pattern.set_extend(cairo.EXTEND_REPEAT)
    return pattern
def make_pattern_circles(col):
    pattern_surface = \
        cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, (0, 0, 6, 6))
    ctx = cairo.Context(pattern_surface)
    #ctx.set_line_width(4)
    ctx.set_source_rgb(col[0],col[1],col[2])
    
    ctx.move_to(0, 0)
    ctx.arc(3, 3, 2.7, 0 * DEGREES, 360 * DEGREES)
    ctx.close_path()
    ctx.fill()
    pattern = cairo.SurfacePattern(pattern_surface)
    pattern.set_extend(cairo.EXTEND_REPEAT)
    return pattern

def fill1(ctx,col,y_offset):
    ctx.set_source_rgb(col[0],col[1],col[2])
    ctx.fill_preserve()
def fill2(ctx,col,y_offset):
    ctx.save()
    ctx.translate(0,y_offset)
    ctx.rotate(45*DEGREES)
    
    ctx.set_source(make_pattern_circles(col))
    ctx.fill_preserve()
    ctx.restore()
def fill3(ctx,col,y_offset):
    ctx.save()
    ctx.translate(0,y_offset)
    ctx.rotate(45*DEGREES)
    
    ctx.set_source(make_pattern_lines(col))
    ctx.fill_preserve()
    ctx.restore()
def fill4(ctx,col,y_offset):
    ctx.set_source_rgb(col[0],col[1],col[2])
fills=[fill1,fill2,fill3,fill4]
def render():
    # create the cairo context      
    width,height =  192,275
    surfaces = [cairo.SVGSurface('./out/4x4_card'+str(x+1)+'.svg', width,height) for x in range(4**4)]
    contexts = [cairo.Context(surface) for surface in surfaces]
    for i in range(4**4):
        color = i%4
        shape = (i//4)%4
        fill = (i//16)%4
        num = i//64
        ctx = contexts[i]
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.save()
        #draw_rounded(ctx, 0,0,width,height, 8)
        ctx.set_source_rgb(1, 1, 1)  # Solid color
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)  # Solid color
        ctx.set_line_width(0.4)
        #ctx.set_dash([10.0, 6.0])
        ctx.stroke()

        ctx.restore()
        for j in y_positions[num]:
            shapes[shape](ctx,width/2.0,j*height,0.38*width,shape_y_rad[shape]*height)
            fills[fill](ctx,colours[color],j*height)
            ctx.set_source_rgb(colours[color][0],colours[color][1],colours[color][2])
            strokes[fill](ctx,8,colours[color])

    # use rsvg to render the cairo context                                      

render()
A4Positions = [[18+185*(i%3),18+(i//3)*266] for i in range (9)]
def collateA4():
    width,height =  595.27559,841.88976
    surfaces = [cairo.PDFSurface('./out/4x4_collate'+str(x+1)+'.pdf', width,height) for x in range(29)]
    contexts = [cairo.Context(surface) for surface in surfaces]
    handle = Rsvg.Handle()
    svgs = [handle.new_from_file(inp) for inp in ['./out/4x4_card'+str(x+1)+'.svg' for x in range(256)]]
    for i in range(256):
        dim = svgs[i].get_dimensions()
        contexts[i//9].save()
        contexts[i//9].translate(A4Positions[i%9][0],A4Positions[i%9][1])
        contexts[i//9].scale(185/dim.width,266/dim.height)
        svgs[i].render_cairo(contexts[i//9])
        contexts[i//9].restore()
collateA4()
def collatedBack():
    width,height =  595.27559,841.88976
    surface = cairo.PDFSurface('./out/back_print_4x4.pdf', width,height)
    context = cairo.Context(surface)
    handle = Rsvg.Handle()
    svg = handle.new_from_file('card_back_4x4.svg')
    dim = svg.get_dimensions()
    
    for i in range(9):
        context.save()
        context.translate(width-A4Positions[i][0]-185,A4Positions[i][1])
        context.scale(185/dim.width,266/dim.height)
        svg.render_cairo(context)
        context.restore()
collatedBack()

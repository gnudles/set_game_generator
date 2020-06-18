#!/usr/bin/env python3                                                          

import random,math
import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg
import cairo

def draw_rounded(cr, x,y,width,height, radius):
    """ draws rectangles with rounded (circular arc) corners """
    degrees = math.pi / 180.0
    cr.arc(x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees)
    cr.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)
    cr.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)  # ;o)
    cr.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)
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
y_positions=[[0.5],[0.38,0.62],[0.26,0.5,0.74]]
shapes = [draw_diamond,draw_oval,draw_star]
shape_y_rad = [0.09,0.07,0.08]
colours = [[0.3,0.6,0.9],[0.9,0.2,0.2],[0.2,0.9,0.4]]
def stroke_normal(ctx,w):
    ctx.set_line_width(w)
    #ctx.set_dash([6.0, 5.0])

    ctx.stroke()
def stroke_dash(ctx,w):
    ctx.set_line_width(w*0.8)
    ctx.set_dash([5.0, 4.5])
    ctx.stroke()
def stroke_two_lines(ctx,w):
    ctx.set_line_width(w)
    ctx.stroke_preserve()
    ctx.set_line_width(w*0.5)
    ctx.set_source_rgb(1, 1, 1)
    ctx.stroke()

strokes=[stroke_two_lines,stroke_dash,stroke_normal]


def make_pattern(col):
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

def fill1(ctx,col):
    ctx.set_source_rgb(col[0],col[1],col[2])
    ctx.fill_preserve()
def fill2(ctx,col):
    ctx.set_source(make_pattern(col))
    ctx.fill_preserve()
def fill3(ctx,col):
    ctx.set_source_rgb(col[0],col[1],col[2])
fills=[fill1,fill2,fill3]
def render():
    # create the cairo context      
    width,height =  192,275
    surfaces = [cairo.SVGSurface('./out/card'+str(x+1)+'.svg', width,height) for x in range(81)]
    contexts = [cairo.Context(surface) for surface in surfaces]
    for i in range(81):
        color = i%3
        shape = (i//3)%3
        num = (i//9)%3
        fill = i//27
        ctx = contexts[i]
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.save()
        draw_rounded(ctx, 0,0,width,height, 10)
        ctx.set_source_rgb(1, 1, 1)  # Solid color
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)  # Solid color
        ctx.set_line_width(1.0)
        ctx.set_dash([10.0, 6.0])
        ctx.stroke()

        ctx.restore()
        for j in y_positions[num]:
            shapes[shape](ctx,96,j*height,75,shape_y_rad[shape]*height)
            
            fills[fill](ctx,colours[color])
            ctx.set_source_rgb(colours[color][0],colours[color][1],colours[color][2])
            strokes[fill](ctx,8)

    # use rsvg to render the cairo context                                      

render()
A4Positions = [[3+197*(i%3),3+(i//3)*279] for i in range (9)]
def collateA4():
    width,height =  595,842
    surfaces = [cairo.PDFSurface('./out/collate'+str(x+1)+'.pdf', width,height) for x in range(9)]
    contexts = [cairo.Context(surface) for surface in surfaces]
    handle = Rsvg.Handle()
    svgs = [handle.new_from_file(inp) for inp in ['./out/card'+str(x+1)+'.svg' for x in range(81)]]
    for i in range(81):
        dim = svgs[i].get_dimensions()
        contexts[i//9].save()
        contexts[i//9].translate(A4Positions[i%9][0],A4Positions[i%9][1])
        contexts[i//9].scale(192/dim.width,275/dim.height)
        svgs[i].render_cairo(contexts[i//9])
        contexts[i//9].restore()
collateA4()

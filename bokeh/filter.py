# -*- coding: utf-8 -*-


import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Div
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.embed import components
from bokeh.io import save

import scipy.signal.windows as ws

def generate_layout():
    # filter name
    filter_name = "Dérivateur"
    
    # initial frequency
    nu0 = 0.1;
    
    # +/- xlim of the plot
    L = 20;
    
    # impulse response
    h = np.array([1,-1])
    
    
    def filt(x, nu, h):
        output = np.zeros(x.shape)
        for k in range(h.shape[0]):
            output = output + np.cos(2*np.pi* (x-k) * nu0) * h[k]
    
        return output
    
    def Hfilt(nu, h):
        output = np.zeros(nu.shape)
        for k in range(h.shape[0]):
            output = output + np.exp(- 2*np.pi * 1j * k * nu) * h[k]
    
        return output
    
    
    
    
    
    
    Nnu = 1000;
    nu = np.linspace(-0.5, 0.5, Nnu)
    
    x = np.linspace(-L, L, 500)
    y = np.cos(2*np.pi*x * nu0)
    y1 = filt(x, nu0, h)
    
    
    H = Hfilt(nu, h)
    
    
    xd = np.arange(-L,L+1)
    yd = np.cos(2*np.pi*xd * nu0)
    y1d = filt(xd, nu0, h)
    
    
    Ylim = np.max([1, np.max(np.abs(H))]) + 0.1
    
    
    
    source_h = ColumnDataSource(data=dict(xh=np.arange(h.shape[0]), h=h))
    
    source_signal = ColumnDataSource(data=dict(x=x, y=y, y1=y1))
    
    source_signal_disc = ColumnDataSource(data=dict(xd=xd,yd=yd,y1d=y1d))
    
    plot_h = figure(x_range=(-L+1, L-1), y_range=(-np.max(np.abs(h))*1.1,np.max(np.abs(h))*1.1) , plot_width=800, plot_height=100, title=filter_name, toolbar_location=None)
    plot_h.circle('xh', 'h', source=source_h, line_width=3, line_alpha=1, size=2, legend_label="RI")
    plot_h.segment('xh', 0, 'xh', 'h', source=source_h, line_width=1, line_alpha=1)
    
    
    plot_signal = figure(x_range=(-L+1, L-1), y_range=(-Ylim, Ylim), plot_width=800, plot_height=300, title=filter_name, toolbar_location=None)
    
    plot_signal.line('x', 'y', source=source_signal, line_width=3, line_alpha=0.2)
    plot_signal.circle('xd', 'yd', source=source_signal_disc, line_width=3, line_alpha=1, size=10, legend_label="Entrée")
    
    plot_signal.line('x', 'y1', source=source_signal, line_width=3, line_alpha=0.2, color="red")
    plot_signal.circle('xd', 'y1d', source=source_signal_disc, line_width=3, line_alpha=1, size=10, color="red", legend_label="Sortie")
    
    
    source_H = ColumnDataSource(data=dict(nu=nu, Habs=np.abs(H), Hphase=np.angle(H)))
    
    source_Hpoint = ColumnDataSource(data=dict(nu0=[nu0], Habs0=np.abs(Hfilt(np.array([nu0]),h)), Hphase0=np.angle(Hfilt(np.array([nu0]),h))))
    plot_Habs = figure(y_range=(-0.1, np.max(np.abs(H)) + 0.1), title="Gain", plot_width=400, plot_height=400, toolbar_location=None)
    plot_Habs.line('nu', 'Habs', source=source_H, line_width=3, line_alpha=0.8)
    
    plot_Habs.circle('nu0', 'Habs0',source=source_Hpoint, size=10)
    
    plot_Hphase = figure(y_range=(-np.pi-0.1, np.pi+0.1), title="Phase",plot_width=400, plot_height=400, toolbar_location=None)
    plot_Hphase.line('nu', 'Hphase', source=source_H, line_width=3, line_alpha=0.8)
    
    plot_Hphase.circle('nu0', 'Hphase0',source=source_Hpoint, size=10)
    
    plot_Habs.xaxis.axis_label = 'Fréquence ν'
    plot_Hphase.xaxis.axis_label = 'Fréquence ν'
    
    
    freq_slider = Slider(start=0, end=0.5, value=nu0, step=.001, title="fréquence")
    
    
    callback = CustomJS(args=dict(source_h=source_h, source_Hpoint=source_Hpoint,source_signal=source_signal, source_signal_disc=source_signal_disc, freq=freq_slider),
                        code="""
    
        const data_signal = source_signal.data;
        const data_signal_disc = source_signal_disc.data;
        const data_point = source_Hpoint.data;
    
        const h = source_h.data['h']
     
        const x = data_signal['x']
        const y1 = data_signal['y1']
    
        
        const xd = data_signal_disc['xd']
        const y1d = data_signal_disc['y1d']
    
    
        const F = freq.value;
        
        const cosf = (t => Math.cos(F * Math.PI * 2 * t))
    
        const Hre = h.reduce((a, v, idx) => a + v * Math.cos(- 2 * Math.PI * idx * F), 0)
        const Him = h.reduce((a, v, idx) => a + v * Math.sin(- 2 * Math.PI * idx * F), 0)
    
        data_point['Habs0'][0] = Math.sqrt(Hre**2 + Him**2)
        data_point['nu0'][0] = F
        data_point['Hphase0'][0] = Math.atan2(Him, Hre)
    
        
         data_signal['y'] = x.map(cosf)
         data_signal_disc['yd'] = xd.map(cosf)
    
        
        for (var i = 0; i < x.length; i++)
        {
             y1[i] = h.reduce((a, hh, idx) => a + cosf(x[i]-idx) * hh, 0)
        }
           
        for (var i = 0; i < xd.length; i++)
        {
            y1d[i] = h.reduce((a, hh, idx) => a + cosf(xd[i]-idx) * hh, 0)
        }
             
        
        source_signal.change.emit();
        source_Hpoint.change.emit();
    
        source_signal_disc.change.emit();
    """)
    freq_slider.js_on_change('value', callback)
    email = Div(text="<p>gilles.chardon@centralesupelec.fr</p>", style={"color": "grey"})
    
    layout = column(plot_h,
          freq_slider,
        plot_signal,
    row(plot_Habs, plot_Hphase), email   
    )
    
    
    return layout


def generate_components():
    return components(generate_layout())

    
def show_layout():    
    show(generate_layout())
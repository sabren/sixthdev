/*
 * Created on Dec 9, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.sabren.boxspring;

import java.awt.Component;
import org.jhotdraw.standard.*;
import org.jhotdraw.framework.*;
import org.jhotdraw.applet.*;
import org.jhotdraw.figures.*;

/**
 * @author michal
 */
public class HelloWorldApplet extends DrawApplet {
	
	private Drawing drawing;
	private DrawingView view;
	private DrawingEditor editor;
	
	public void init() {
		buildDrawing();
		editor = new NullDrawingEditor();
		view = new StandardDrawingView(editor, getWidth(), getHeight());
		view.setDrawing(this.drawing);
		getContentPane().add((Component) view);
	}

	/**
	 * 
	 */
	private void buildDrawing() {
		drawing = new StandardDrawing();
		TextFigure text = new TextFigure();
		text.setText("hello, world");
		drawing.add(text);
	}
}

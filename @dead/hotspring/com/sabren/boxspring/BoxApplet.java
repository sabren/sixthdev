/*
 * Created on Dec 9, 2004
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
public class BoxApplet extends DrawApplet {
	
	private Drawing drawing;
	private DrawingView view;
	private BoxDrawingEditor editor;
	
	public void init() {
		buildDrawing();
		editor = new BoxDrawingEditor();
		view = new StandardDrawingView(editor, getWidth(), getHeight());
		editor.setDrawingView(view);
		view.setDrawing(this.drawing);
		getContentPane().add((Component) view);
	}

	/**
	 * 
	 */
	private void buildDrawing() {
		drawing = new StandardDrawing();			
		drawing.add(new BoxFigure("hello, world!"));
	}
}

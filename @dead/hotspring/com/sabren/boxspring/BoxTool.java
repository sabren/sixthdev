/*
 * Created on Dec 9, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.sabren.boxspring;

import java.awt.Point;
import java.awt.event.MouseEvent;

import org.jhotdraw.framework.*;
import org.jhotdraw.standard.*;

/**
 * @author michal
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class BoxTool extends AbstractTool {

	/**
	 * @param newDrawingEditor
	 */
	public BoxTool(DrawingEditor newDrawingEditor) {
		super(newDrawingEditor);
		// TODO Auto-generated constructor stub
	}
	
	public void mouseUp(MouseEvent e, int x, int y) {		
		if (e.getClickCount() == 2) {
			BoxFigure box = new BoxFigure("added");
			box.displayBox(new Point(x, y), new Point(x+50, y+10));
			DrawingView view = (DrawingView) e.getSource();
			view.add(box);			
		}
	}

}
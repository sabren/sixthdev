/*
 * Created on Dec 9, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.sabren.boxspring;

import org.jhotdraw.framework.*;
import org.jhotdraw.standard.*;
import org.jhotdraw.util.UndoManager;

/**
 * @author michal
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class NullDrawingEditor implements DrawingEditor {

	/**
	 * 
	 */
	public NullDrawingEditor() {		
	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.DrawingEditor#view()
	 */
	public DrawingView view() {
		// TODO Auto-generated method stub
		return null;
	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.DrawingEditor#views()
	 */
	public DrawingView[] views() {
		// TODO Auto-generated method stub
		return null;
	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.DrawingEditor#tool()
	 */
	public Tool tool() {
		return new NullTool(this);
	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.DrawingEditor#toolDone()
	 */
	public void toolDone() {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.FigureSelectionListener#figureSelectionChanged(org.jhotdraw.framework.DrawingView)
	 */
	public void figureSelectionChanged(DrawingView view) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.DrawingEditor#addViewChangeListener(org.jhotdraw.framework.ViewChangeListener)
	 */
	public void addViewChangeListener(ViewChangeListener vsl) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.DrawingEditor#removeViewChangeListener(org.jhotdraw.framework.ViewChangeListener)
	 */
	public void removeViewChangeListener(ViewChangeListener vsl) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.DrawingEditor#showStatus(java.lang.String)
	 */
	public void showStatus(String string) {
		// TODO Auto-generated method stub

	}

	/* (non-Javadoc)
	 * @see org.jhotdraw.framework.DrawingEditor#getUndoManager()
	 */
	public UndoManager getUndoManager() {
		// TODO Auto-generated method stub
		return null;
	}

}

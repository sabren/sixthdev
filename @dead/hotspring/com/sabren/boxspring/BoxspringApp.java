/*
 * Created on Dec 9, 2004
 *
 * Boxspring: a little node editor written with jhotdraw
 *
 */
package com.sabren.boxspring;
import javax.swing.JToolBar;

import org.jhotdraw.application.DrawApplication;
import org.jhotdraw.standard.CreationTool;
import org.jhotdraw.framework.Tool;

/**
 * @author michal
 * the main application class
 */
public class BoxspringApp extends DrawApplication {

	public BoxspringApp() {
		super("Boxspring");
	}

	protected void createTools(JToolBar palette) {
		Tool tool = new CreationTool(this, new BoxFigure("asdf"));
		palette.add(createToolButton(IMAGES + "BOX", "Box Tool", tool));
	}
	
	public static void main(String[] args) {
		DrawApplication window = new BoxspringApp();
		window.open();
	}
}

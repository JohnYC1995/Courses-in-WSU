import java.awt.*;
import java.util.*;
import java.applet.*;
import java.awt.event.MouseEvent;
import javax.swing.event.*;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import java.io.File;
import org.json.simple.JSONArray; 
import org.json.simple.JSONObject; 
import org.json.simple.parser.JSONParser; 
import org.json.simple.parser.ParseException; 
/*<applet code="Main" height=400 width=400></applet>*/

public class Main extends Applet implements Runnable
{
/* Configuration arguments. These should be initialized with the values read from the config.JSON file*/					
    private int numBalls;
/*end of config arguments*/
    private int refreshrate = 15;	           //Refresh rate for the applet screen. Do not change this value. 
	private boolean isStoped = true;
    Font f = new Font ("Arial", Font.BOLD, 18);
	private Player player;			           //Player instance.
	private Ball redball;                      //Ball instance. You need to replace this with an array of balls.     
	private BounceBall B_Ball;
	private ShrinkBall S_Ball;
	public int lifenum;
	private int X;
	private int mouseclick_num = 1;
	private int number_b;
	private int shrink_rate;
	private int[] radius = new int[3];
	private int[] initXpos = new int[3];
	private int[] initYpos = new int[3];
	private int[] speedX = new int[3];
	private int[] speedY = new int[3];
	private int[] maxBallSpeed = new int[3];
	Thread th;						           //The applet thread. 
    Cursor c;				
    private GameWindow gwindow;                 // Defines the borders of the applet screen. A ball is considered "out" when it moves out of these borders.
	private Image dbImage;
	private Graphics dbg;
	private int count_for_ball;
	//private  ArrayList<Ball> Balllist=new ArrayList<Ball>();

	class HandleMouse extends MouseInputAdapter 
	{
    	public HandleMouse() 
    	{
            addMouseListener(this);
        }	
    	public void mouseClicked(MouseEvent e) 
    	{
        	if (!isStoped) {
        		mouseclick_num += e.getClickCount();
        		
				if (redball.userHit (e.getX(), e.getY())) {
					redball.ballWasHit ();
	        	}
				if (B_Ball.userHit (e.getX(), e.getY())){
					B_Ball.ballWasHit();
				}
				if (S_Ball.userHit(e.getX(), e.getY())){
					S_Ball.ballWasHit();
				}
			}
			else if (isStoped && e.getClickCount() == 2) {
				isStoped = false;
				init ();
			}
    	}
    	public void mouseReleased(MouseEvent e) 
    	{  
    	}
        
    	public void RegisterHandler() 
    	{
    	}
    }
	
	HandleMouse hm = new HandleMouse();
	
	//JSON reader; you need to complete this function
	public void JSONReader()
	{
		String filePath = "/Users/Juhn/Desktop/Classes/Undertaking/CPTS355/HW6/BallGame_skeleton/config.JSON";
		try {
			// read the json file
			FileReader reader = new FileReader(filePath);
			JSONParser jsonParser = new JSONParser();
			JSONObject jsonObject = (JSONObject) jsonParser.parse(reader);

			//*handle a GameWindow structure into the json object
			JSONObject structure_gw = (JSONObject) jsonObject.get("GameWindow");
			int Newx_leftout=Integer.valueOf((String)structure_gw.get("x_leftout"));
			int Newx_rightout=Integer.valueOf((String)structure_gw.get("x_rightout"));
			int Newy_upout=Integer.valueOf((String)structure_gw.get("y_upout"));
			int Newy_downout=Integer.valueOf((String)structure_gw.get("y_downout"));
			this.gwindow=new GameWindow(Newx_leftout,Newx_rightout,Newy_upout,Newy_downout);
			
			// handle a Player structure into the json object
			JSONObject structure_player = (JSONObject) jsonObject.get("Player");
			this.lifenum = 	Integer.valueOf((String) structure_player.get("numLives"));
			this.X = Integer.valueOf((String)structure_player.get("score2EarnLife"));
			
			//*get a String from the JSON object
			String numballs = (String) jsonObject.get("numBalls");
			this.numBalls=Integer.valueOf(numballs);		

			// get an array from the JSON object
			JSONArray ball= (JSONArray) jsonObject.get("Ball");
			
			Iterator i = ball.iterator();
			// take each value from the json array separately
			while (i.hasNext()) {
				JSONObject innerObj = (JSONObject) i.next();
				int Newradius=Integer.valueOf((String) innerObj.get("radius"));
				int NewinitXpos=Integer.valueOf((String) innerObj.get("initXpos"));
				int NewinitYpos=Integer.valueOf((String) innerObj.get("initYpos"));
				int NewspeedX=Integer.valueOf((String) innerObj.get("speedX"));
				int NewspeedY=Integer.valueOf((String) innerObj.get("speedY"));
				int NewmaxBallSpeed=Integer.valueOf((String) innerObj.get("maxBallSpeed"));
				if(innerObj.get("id").equals("1")) {
					this.radius[0] = Newradius;
					this.initXpos[0] = NewinitXpos;
					this.initYpos[0] = NewinitYpos;
					this.speedX[0] = NewspeedX;
					this.speedY[0] = NewspeedY;
					this.maxBallSpeed[0] = NewmaxBallSpeed;
				}
				if(innerObj.get("id").equals("2")) {
					this.radius[1] = Newradius;
					this.initXpos[1] = NewinitXpos;
					this.initYpos[1] = NewinitYpos;
					this.speedX[1] = NewspeedX;
					this.speedY[1] = NewspeedY;
					this.maxBallSpeed[1] = NewmaxBallSpeed;
					this.number_b = Integer.valueOf((String)innerObj.get("bounceCount"));
				}
				if(innerObj.get("id").equals("3")) {
					this.radius[2] = Newradius;
					this.initXpos[2] = NewinitXpos;
					this.initYpos[2] = NewinitYpos;
					this.speedX[2] = NewspeedX;
					this.speedY[2] = NewspeedY;
					this.maxBallSpeed[2] = NewmaxBallSpeed;
					this.shrink_rate =Integer.valueOf((String)innerObj.get("shrinkRate"));

				}
			}
		} catch (FileNotFoundException ex) {
			ex.printStackTrace();
		} catch (IOException ex) {
			ex.printStackTrace();
		} catch (ParseException ex) {
			ex.printStackTrace();
		} catch (NullPointerException ex) {
			ex.printStackTrace();
		}	
	}

	/*initialize the game*/
	public void init ()
	{	
		//reads info from JSON doc
		this.JSONReader();
		c = new Cursor (Cursor.CROSSHAIR_CURSOR);
		this.setCursor (c);	
		setBackground (Color.black);
		setFont (f);
		if (getParameter ("refreshrate") != null) {
			refreshrate = Integer.parseInt(getParameter("refreshrate"));
		}
		else refreshrate = 15;
		player = new Player ();
		player.Player_maxlife(lifenum);
		player.bonusgap(X);
		/* The parameters for the GameWindow constructor (x_leftout, x_rightout, y_upout, y_downout) 
		should be initialized with the values read from the config.JSON file*/	
		this.setSize(gwindow.x_rightout, gwindow.y_downout); //set the size of the applet window.
		/*The skeleton code creates a single basic ball. Your game should support arbitrary number of balls. 
		* The number of balls and the types of those balls are specified in the config.JSON file.
		* The ball instances will be stores in an Array or Arraylist.  */
		/* The parameters for the Ball constructor (radius, initXpos, initYpos, speedX, speedY, maxBallSpeed, color) 
		should be initialized with the values read from the config.JSON file. Note that the "color" need to be initialized using the RGB values provided in the config.JSON file*/
		redball =  new Ball(radius[0], initXpos[0], initYpos[0], speedX[0], speedY[0], maxBallSpeed[0], Color.red, player, gwindow,player.getlife());
		B_Ball = new BounceBall(radius[1], initXpos[1], initYpos[1], speedX[1], speedY[1], maxBallSpeed[1], Color.blue, player, gwindow,number_b);
		S_Ball = new ShrinkBall(radius[2], initXpos[2], initYpos[2], speedX[2], speedY[2], maxBallSpeed[2], Color.yellow, player, gwindow,player.getlife(),shrink_rate);
	}
	
	/*start the applet thread and start animating*/
	public void start ()
	{		
		if (th==null){
			th = new Thread (this);
		}
		th.start ();
	}
	
	/*stop the thread*/
	public void stop ()
	{
		th=null;
	}
	public void run ()
	{	
		/*Lower this thread's priority so it won't interfere with other processing going on*/
		Thread.currentThread().setPriority(Thread.MIN_PRIORITY);

        /*This is the animation loop. It continues until the user stops or closes the applet*/
		while (true) {

			if (!isStoped) {
				redball.move();
				B_Ball.move();
				S_Ball.move();
			}
            /*Display it*/
			repaint();           
			try {	
				Thread.sleep (refreshrate);
			}
			catch (InterruptedException ex) {
				
			}			
		}
	}

	public void paint (Graphics g)
	{
		/*if the game is still active draw the ball and display the player's score. If the game is active but stopped, ask player to double click to start the game*/ 
		if (!player.isGameOver()) {
			g.setColor (Color.yellow);
			g.drawString ("Score: " + player.getScore(), 50, 40);
			g.drawString("Lives: " + player.getlife(), 150, 40); // The player lives need to be displayed
			g.drawString("Baseball: " + player.getbaseball(),300,40);
			g.drawString("Bounceball: " + player.getbounceball(),430,40);
			g.drawString("Shrinkball: " + player.getshrinkball(),580,40);
			g.drawString("bounce numbers: "+B_Ball.currbouncetime() + "%" +number_b, 720, 40);
			redball.DrawBall(g);
			B_Ball.DrawBall(g);
			S_Ball.DrawBall(g);
			if (isStoped) {
				g.setColor (Color.yellow);
				g.drawString ("Doubleclick on Applet to start Game!", 300, 200);
			}
		}

		/*if the game is over (i.e., the ball is out) display player's score*/
		else {
			g.setColor (Color.yellow);
			g.drawString ("Game over!", 130, 100);
			g.drawString ("You scored " + player.getScore() + " Points!", 90, 140);
			g.drawString("Statistics: ", 400, 160);
			g.drawString("Number of Clicks: "+mouseclick_num, 400, 180); // The number of clicks need to be displayed
			g.drawString( "% of Successful Clicks: " +player.getSucshits()+ "%"+mouseclick_num,400,200); // The % of successful clicks need to be displayed
			g.drawString("Ball most hit: "+ player.getmosthitball(), 400, 240); // The nball that was hit the most need to be displayed
			g.drawString ("Doubleclick on the Applet, to play again!", 300, 300);
			isStoped = true;	
		}
	}

	public void update (Graphics g)
	{
		if (dbImage == null)
		{
			dbImage = createImage (this.getSize().width, this.getSize().height);
			dbg = dbImage.getGraphics ();
		}
		dbg.setColor (getBackground ());
		dbg.fillRect (0, 0, this.getSize().width, this.getSize().height);

		
		dbg.setColor (getForeground());
		paint (dbg);

		
		g.drawImage (dbImage, 0, 0, this);
	}
}



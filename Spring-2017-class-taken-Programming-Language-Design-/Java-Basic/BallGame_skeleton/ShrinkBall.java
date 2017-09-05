import java.applet.*;
import java.awt.*;
import java.util.Random;


public class ShrinkBall
{
    /*Properties of the basic ball. These are initialized in the constructor using the values read from the config.xml file*/
	protected  int pos_x;			
	protected int pos_y; 				
	protected int radius;
	protected int first_x;			
	protected int first_y;					
	protected int x_speed;			
	protected int y_speed;			
	protected int maxspeed;
	protected int conut_for_b;
	private int count_s_out;
	protected int number_life;
	private Random random = new Random();
	private int org_radius;
	private int count_b = 1;
	private int shrink_r ;
	Color color;
	
    GameWindow gameW;
	Player player;
	
	/*constructor*/
	public ShrinkBall (int radius, int initXpos, int initYpos, int speedX, int speedY, int maxBallSpeed, Color color, Player player,  GameWindow gameW,int lifenum,int shrink_rate)
	{	
		this.radius = radius;
		shrink_r = shrink_rate;
		org_radius = radius;
		pos_x = initXpos;
		pos_y = initYpos;
		
		first_x = initXpos;
		first_y = initYpos;

		x_speed = speedX;
		y_speed = speedY;

		maxspeed = maxBallSpeed;
		count_s_out = 1;
		number_life=lifenum;
		this.color = color;

		this.player = player;
		this.gameW = gameW;

	}

	/*update ball's location based on it's speed*/
	public void move ()
	{
		pos_x += x_speed;
		pos_y += y_speed;
		isOut();
	}

	/*when the ball is hit, reset the ball location to its initial starting location*/
	public void ballWasHit ()
	{	
		player.countsball();
		count_b +=1;
		resetBallPosition();
		x_speed = random.nextInt(5)%(5-(-2)+1) + (-2);
		y_speed = random.nextInt(5)%(5-(-2)+1) + (-2);
		this.radius = (this.radius*(100-shrink_r))/100;
		if (this.radius<org_radius*3/10){
			this.radius = org_radius;
			count_b =1;
		}
	}
	public boolean Ballisout(){
		if ((pos_x < gameW.x_leftout) || (pos_x > gameW.x_rightout) || (pos_y < gameW.y_upout) || (pos_y > gameW.y_downout)) {	
			return true;
		}	
		else return false;
	}
	/*check whether the player hit the ball. If so, update the player score based on the current ball speed. */	
	public boolean userHit (int maus_x, int maus_y)
	{
		
		double x = maus_x - pos_x;
		double y = maus_y - pos_y;

		double distance = Math.sqrt ((x*x) + (y*y));
		
		if (Double.compare(distance-this.radius , player.scoreConstant + Math.abs(x_speed)) <= 0)  {
			player.addScore (player.scoreConstant * count_b);
			return true;
		}
		else return false;
	}

    /*reset the ball position to its initial starting location*/
	protected void resetBallPosition()
	{
		pos_x = (gameW.x_rightout+gameW.x_leftout)/2;
		pos_y = (gameW.y_upout+gameW.y_downout)/2;
	}

	/*check if the ball is out of the game borders. if so, game is over!*/ 
	protected boolean isOut ()
	{
		if ((pos_x < gameW.x_leftout) || (pos_x > gameW.x_rightout) || (pos_y < gameW.y_upout) || (pos_y > gameW.y_downout)) {	
			resetBallPosition();
			count_s_out +=1;
			x_speed = random.nextInt(5)%(5-(-2)+1) + (-2);
			y_speed = random.nextInt(5)%(5-(-2)+1) + (-2);
			if (count_s_out>number_life){
				player.gameIsOver();
			}
			player.minuslife();
			return true;
		}	
		else return false;
	}

	/*draw ball*/
	public void DrawBall (Graphics g)
	{
		g.setColor (color);
		g.fillOval (pos_x - radius, pos_y - radius, 2 * radius, 2 * radius);
	}

}

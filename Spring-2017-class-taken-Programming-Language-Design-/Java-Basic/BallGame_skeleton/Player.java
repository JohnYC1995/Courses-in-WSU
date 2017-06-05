public class Player
{
	
	private int score;			   //player score
	private int tem_score;
	private int life;
	private int X;
	private int hitsnum=0;
	private int count_red=0;
	private int count_b = 0;
	private int count_s = 0;
	private boolean gameover=false;	
	public int scoreConstant = 10; //This constant value is used in score calculation. You don't need to change this. 		

	public Player()
	{
		score = 0; //initialize the score to 0
	}
	
	public void Player_maxlife(int maxlife){
		 life = maxlife;
	}
	
	
	public void bonusgap(int gap){
		X = gap;
	}
	/* get player score*/
	public int getScore ()
	{
		return score;
	}
	public int getlife ()
	{

		return life;
	}
	public int getSucshits(){
		return hitsnum;

	}
	
	/*check if the game is over*/
	public boolean isGameOver ()
	{
		return gameover;
	}
	public void countredball(){
		count_red +=1;
		
	}
	public void countbball(){
		count_b +=1;
	}
	public void countsball(){
		count_s +=1;
	}
	public int getbaseball(){
		return count_red;
	}
	public int getbounceball(){
		return count_b;
	}
	public int getshrinkball(){
		return count_s;
	}
	public String getmosthitball(){
		
		if (count_red>count_b||count_red>count_s){
			return "baseball";
		}
		if (count_b>count_red||count_b>count_s){
			return "bounceball";
		}
		if (count_s>count_b||count_s>count_red){
			return "shrinkball";
		}
		else{
			return "all ball have equal hit number";
		}
	}

	/*update player score*/
	public void addScore (int plus)
	{	tem_score = score;
		if(tem_score % X==0 && tem_score>0){
			life+=1;
			tem_score = 0;
			
		}
		hitsnum+=1;
		score += plus;
		
	}

	/*update player life*/
	public void minuslife(){
		life -=1;
		if (life <0){
			gameIsOver ();
		}
	}
	/*update "game over" status*/
	public void gameIsOver ()
	{
		gameover = true;
	}
}
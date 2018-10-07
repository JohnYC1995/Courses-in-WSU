# - Contents

```
1. CPT S355 Programming Language Design
2. CPT S540 Artificial Intelligence
3. CPT S580 Reinforcement Learning
```

# 1. CPT S355 Programming Language Design

Six different programming languages including Python, Java, C++, Scheme, Standard-ML, Postscript-interpreter are taught in this class.

## Oragnization of this part of the code

* **There are six sets of homework. For each homework, using a kind of language to approach similar problems.

## Acknowledge
Here I want specifically thanks for professor Ay's teaching.

# 2. CPT S540 Artificial Intelligence

Implementation of classical Artificial Intelligence algorithms on a classic game - Wumpus World.

* ** To run this agent, one just need to compile ```wumpsim.cc``` file, the agent will generate results based on your algorithms.
* ** To see my strategy, please take a look the ```Agent.cc``` and ```Agent.h``` files. Feel free to modify the code to satisfy your agent.

## Ackonwledge
A C++ Wumpus World simulator, following the rules from the textbook ``Artificial intelligence A Modern Approach``, is available at prof. Larry Holder’s teaching website, ```http://www.eecs.wsu.edu/~holder/courses/AI/wumpus```

# 3. CPT S580 Reinforcement Learning

All the code implemented in this class.

## Oragnization of the code

* **There are three times homeworks and a final project. For each homework, I implement a certain method of Reinforcement Learning.
* **The final project is a collaberation work. Our group members are Tao Zeng, Zhang Yan, Yongjun Chen. In our works, we try to implement the object detection task in the neural images using Deep Q-learning methods.

## Summary of Final Project 

![images](https://github.com/JohnYC1995/Courses-in-WSU/blob/master/Spring-2017-class-taken-Reinforcement-Learning/Sample_process_images/Natural_images_process.png)
```
Illustration of the process that agent attempted to detect the object. Green boxes represent
the ground truth bounding boxes; Red box denotes current objective box that agent is trying localize.
White boxes shows that prediction box produced by agent in current step according to the Q-value.
The white boxes in left column illustrates the location where agent starts from. After continuously 60
actions without getting trigger, agent will restart. The middle column show the restart bounding box.
The right column showed the bounding box that agent reach the trigger state.
```
![images](https://github.com/JohnYC1995/Courses-in-WSU/blob/master/Spring-2017-class-taken-Reinforcement-Learning/Sample_process_images/Neural_image_result.png)
```
Illustration of active localization on EM neuron image. Red box denotes the ground truth
of neuron locations. White Box shows the localization result produced by the agent. Blue box: an
example that shows an initial starting box for the agent in one of locations.
```
## Reference

The code was implemented based on the book Reinforcement Learning: An Introduction:(https://mitpress.mit.edu/books/reinforcement-learning). 

## Acknowledge
This course is taken in 2017 Spring, it's quite interesting class. Here I want to specifically thanks to Tao Zeng who has helped me a lot to learn python programming.

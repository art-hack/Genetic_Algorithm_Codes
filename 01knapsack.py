import random
import matplotlib.pyplot as plt
import time
import sys

value=list()
weight=list()
MAX_WEIGHT = 0

def fitness_value(gene):
  conflicts = 0
  for i in range(len(gene)):
    if(gene[i]==1):
      conflicts += value[i]
  return conflicts


def filter(gene):
  added_sum=0
  global MAX_WEIGHT
  new_gene=list()
  for i in range(len(gene)):
    if((added_sum+weight[i])<=MAX_WEIGHT and gene[i]==1):
      added_sum += weight[i]
      new_gene.append(1)
    else:
      new_gene.append(0)
  return new_gene


def generate(n,length):
  population = list()
  te=list()
  for j in range(length):
    te.append(random.randint(0,1))
  population.append(filter(te))

  for i in range(n-1):
    temp=list()
    for j in range(length):
      temp.append(random.randint(0,1))
    population.append(filter(temp))
  return population


def crossover(gene1,gene2):
  N = random.randint(0,len(gene1)-1)
  for i in range(N,len(gene1)):
    gene1[i],gene2[i] = gene2[i],gene1[i]
  return filter(gene1),filter(gene2)


def mutate(gene):
  if(random.uniform(0, 1)<0.5):
    a = random.randint(0,len(gene)-1)
    gene[a] = int((gene[a]+1)%2)
  return filter(gene)


def main():
  N = int(input("Enter Number of objects: "))
  start_time = time.process_time()
  global MAX_WEIGHT
  temp = int(1000)
  for i in range(N):
    a = random.randint(10,20)
    temp = min(temp,a)
    weight.append(a)
    value.append(random.randint(10,20))
  MAX_WEIGHT = int(10*temp)
  
  print("Weights: ",end="")
  for i in range(N):
    print(weight[i],end=" ")
  print()
  print("Values: ",end="")
  for i in range(N):
    print(value[i],end=" ")
  print()
  print("Capacity: ",MAX_WEIGHT)
  print()
  population = generate(500,N)
  population = sorted(population,reverse=True,key=fitness_value)
  x = list()
  y = list()
  MAX_GENERATIONS = int(500)
  for i in range(1,MAX_GENERATIONS+1):
    print("Generation ",i," with fitness value: ",fitness_value(population[0]),end='\r')
    if((i%100)==0):
      print()
    sys.stdout.flush()
    gene1 = population[random.randint(0,499)]
    for j in range(1):
      gen = population[random.randint(0,499)]
      if(fitness_value(gen)<fitness_value(gene1)):
        gene1 = gen
    
    gene2 = population[random.randint(0,499)]
    for j in range(1):
      gen = population[random.randint(0,499)]
      if(fitness_value(gen)<fitness_value(gene2)):
        gene2 = gen
    
    if(random.randint(0,99)>70):
      gene1,gene2 = crossover(gene1,gene2)
      gene1 = mutate(gene1)
      gene2 = mutate(gene2)
      population.append(gene1)
      population.append(gene2)
      population = sorted(population,reverse=True,key=fitness_value)

    while(len(population)>500):
      population.pop()
    x.append(i)
    y.append(fitness_value(population[0]))

  print()
  print("Best Solution found in " + str(MAX_GENERATIONS) + " generations ")
  print("Max fitness value achieved: ",fitness_value(population[0]))
  print("Objects Selected: ",end="")
  sumed = int(0)
  for i in range(N):
    if(population[0][i]==1):
      print(i+1,end=" ")
      sumed+=value[i]
  print()
  print("Total value Achieved: ",sumed)


  print("Total time taken: %s seconds" % (time.process_time() - start_time))
  plt.plot(x, y)
  plt.xlabel('Generation')
  plt.ylabel('Fitness Value')
  plt.title('Fitness Function Graph')
  plt.show()

random.seed(454)
main()
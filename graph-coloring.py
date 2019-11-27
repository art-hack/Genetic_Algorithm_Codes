import random
import matplotlib.pyplot as plt
import time
import sys

adj = list()

def fitness_value(gene):
  conflicts =0
  for i in range(len(adj)):
    for j in range(len(adj[i])):
      if(adj[i][j]==1 and i!=j):
        if(gene[i]==gene[j]):
          conflicts+=1
  return (conflicts/2)


def generate(n,color,length):
  population = list()
  te=list()
  for j in range(length):
    te.append(random.randint(0,color-1))
  population.append(te)

  for i in range(n-1):
    temp=list()
    for j in range(length):
      temp.append(random.randint(0,color-1))
    population.append(temp)
  return population


def crossover(gene1,gene2):
  N = int(len(gene1)/2)
  gen = gene2[N:]
  gen.extend(gene1[0:N])
  gen2 = gene1[N:]
  gen2.extend(gene2[0:N])
  return gen,gen2


def mutate(gene):
  if(random.uniform(0, 1)<0.5):
    a = random.randint(0,len(gene)-1)
    gene[a]=random.randint(0,4)
  return gene


def generate_graph(N,M):
  for i in range(N):
    te = list()
    for j in range(N):
      te.append(0)
    adj.append(te)

  for i in range (M):
    xx = random.randint(0,N-1)
    xxx = random.randint(0,N-1)
    adj[xx][xxx]=1
    adj[xxx][xx]=1


def main():
  start_time = time.process_time()
  N = 20
  print("No of Nodes on the Graph: 20")
  print("No of Undirected Edges on the Graph: 50")
  print("No of Colors on the Graph: 5")
  generate_graph(20,50)
  print()
  print("Generated Adjacency Matrix")
  for i in range(N):
    for j in range(N):
      print(adj[i][j],end=" ")
    print()
  print()
  population = generate(20,5,20)
  population = sorted(population,key=fitness_value)
  flag = 1
  x = list()
  y = list()
  MAX_GENERATIONS = int(10000)
  for i in range(1,MAX_GENERATIONS+1):
    if(fitness_value(population[0])==0):
      print()
      print("Solution found at generation ",i)
      flag = 0
      for j in range(0,N):
        print(population[0][j],end=" ")
      print()
      break

    print("Generation ",i," with fitness value: ",fitness_value(population[0]),end='\r')
    if((i%100)==0):
      print()
    sys.stdout.flush()
    gene1 = population[random.randint(0,19)]
    for j in range(4):
      gen = population[random.randint(0,19)]
      if(fitness_value(gen)<fitness_value(gene1)):
        gene1 = gen
    
    gene2 = population[random.randint(0,19)]
    for j in range(4):
      gen = population[random.randint(0,19)]
      if(fitness_value(gen)<fitness_value(gene2)):
        gene2 = gen
    
    gene1,gene2 = crossover(gene1,gene2)
    gene1 = mutate(gene1)
    gene2 = mutate(gene2)
    population.append(gene1)
    population.append(gene2)
    population = sorted(population,key=fitness_value)
    while(len(population)>20):
      population.pop()
    x.append(i)
    y.append(fitness_value(population[0]))

  if(flag==1):
    print()
    print("Best solution found with fitness value: ",fitness_value(population[0]))
    for j in range(N):
      print(population[0][j],end=" ")
    print()
  print("Total time taken: %s seconds" % (time.process_time() - start_time))
  plt.plot(x, y)
  plt.xlabel('Generation')
  plt.ylabel('Fitness Value')
  plt.title('Fitness Function Graph')
  plt.show()

random.seed(36)
main()
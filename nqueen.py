import random
import matplotlib.pyplot as plt 
import sys


def fitness_value(gene):
  diag1 = dict()
  diag2 = dict()
  for i in range(1,len(gene)+1):
    t = i+gene[i-1]
    if t in diag1:
      diag1[t] += 1
    else:
      diag1[t] = 1

    t = i-gene[i-1]
    if t in diag2:
      diag2[t] += 1
    else:
      diag2[t] = 1
  
  conflicts = 0
  for i in diag1.keys():
    if(diag1[i]>1):
      conflicts += ((diag1[i]*(diag1[i]-1))/2)
  
  for i in diag2.keys():
    if(diag2[i]>1):
      conflicts += ((diag2[i]*(diag2[i]-1))/2)
    
  return conflicts


def bisect(lst, value, key=None):
    if key is None:
        key = lambda x: x
    def bis(lo, hi=len(lst)):
        while lo < hi:
            mid = (lo + hi) // 2
            if key(lst[mid]) < value:
                lo = mid + 1
            else:
                hi = mid
        return lo
    return bis(0)


def insert(gene, population):
  val = fitness_value(gene)
  val2 = bisect(population,val,fitness_value)
  p = population[0:val2]
  p.append(gene)
  p.extend(population[val2:])
  return p


def generate(n,length):
  population = list()
  te=list()
  for j in range(length):
    te.append(j+1)
  population.append(te)

  for i in range(n-1):
    temp=list()
    for j in range(length):
      temp.append(j+1)
    random.shuffle(temp)
    random.shuffle(temp)
    population = insert(temp,population)
  return population


def crossover(gene1,gene2):
  N = int(len(gene1))
  gen = gene1[0:int((N+1)/2)]
  start = int((N+1)/2)
  while(len(gen)!=len(gene1)):
    if gene2[start] not in gen:
      gen.append(gene2[start])
    start = (start+1)%len(gene1)

  gen2 = gene2[0:int((len(gene2)+1)/2)]
  start = int((len(gene2)+1)/2)
  while(len(gen2)!=len(gene2)):
    if gene1[start] not in gen2:
      gen2.append(gene1[start])
    start = (start+1)%len(gene2)

  return gen,gen2


def mutate(gene):
  if(random.uniform(0, 1)<0.5):
    a = random.randint(0,len(gene)-1)
    b = random.randint(0,len(gene)-1)
    get = gene[a],gene[b]
    gene[b],gene[a]=get
  return gene

def main():
  N = int(input("Enter Number of Queens on Board: "))
  population = generate(100,N)
  flag = 1
  x = list()
  y = list()
  MAX_GENERATIONS = int(10000)
  for i in range(1,MAX_GENERATIONS+1):
    if(fitness_value(population[0])==0):
      print()
      print("Solution found at generation ",i)
      flag = 0
      for j in range(1,N+1):
        for k in range(1,N+1):
          if(k==population[0][j-1]):
            print('Q',end="")
          else:
            print('.',end="")
        print()
      break
    print("Generation ",i," with fitness value: ",fitness_value(population[0]),end='\r')
    sys.stdout.flush()
    gene1 = population[random.randint(0,99)]
    for j in range(4):
      gen = population[random.randint(0,99)]
      if(fitness_value(gen)<fitness_value(gene1)):
        gene1 = gen
    
    gene2 = population[random.randint(0,99)]
    for j in range(4):
      gen = population[random.randint(0,99)]
      if(fitness_value(gen)<fitness_value(gene2)):
        gene2 = gen
    
    gene1,gene2 = crossover(gene1,gene2)
    gene1 = mutate(gene1)
    gene2 = mutate(gene2)
    population = insert(gene1,population)
    population = insert(gene2,population)
    while(len(population)>100):
      population.pop()
    x.append(i)
    y.append(fitness_value(population[0]))

  if(flag==1):
    print()
    print("Solution not found in " + str(MAX_GENERATIONS) + " generations ")
    print("Best solution found with fitness value: ",fitness_value(population[0]))
    for j in range(1,N+1):
      for k in range(1,N+1):
        if(k==population[0][j-1]):
          print('Q',end="")
        else:
          print('.',end="")
      print()

  plt.plot(x, y)
  plt.xlabel('Generation')
  plt.ylabel('Fitness Value')
  plt.title('Fitness Function Graph')
  plt.show()

random.seed(545)
main()
import random
import math
import matplotlib.pyplot as plt

k = 7 # number of clusters (max = 7)
n = 500 # number of data_points

color = ['b','g','r','c','m','y','k','w']
E = []
C = []
L = {}


#Create random 3D-Datapoints
for i in range(n):
    random_x = random.randint(0,100)
    random_y = random.randint(0,100)
    random_z = random.randint(0,100)
    point = (random_x, random_y, random_z)
    E.append(point)


def plot(plotClusters, colorDataPoints, title):
    X_D = []
    Y_D = []
    Z_D = []
  
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('x')
    ax.set_xlabel('y')
    ax.set_xlabel('z')
    
    if plotClusters:
        X_C = []
        Y_C = []
        Z_C = []

        for x,y,z in C:
            X_C.append(x)
            Y_C.append(y)
            Z_C.append(z)

        for i,c in enumerate(C):
            ax.scatter(X_C[i], Y_C[i], Z_C[i], s = 200, c = color[i], marker = "x")

    if not colorDataPoints:
        for x,y,z in E:
            X_D.append(x)
            Y_D.append(y)
            Z_D.append(z)

        ax.scatter(X_D, Y_D, Z_D, s = 30, c = 'k', marker = "o")
    else:
        pts = []

        for i,c in enumerate(C):
            pts.clear()
            X_D.clear()
            Y_D.clear()
            Z_D.clear()

            for l in L:
                if L[l] == i:
                    pts.append(l)

            for x,y,z in pts:
                X_D.append(x)
                Y_D.append(y)
                Z_D.append(z)

            ax.scatter(X_D, Y_D, Z_D, s = 30, c = color[i], marker = "o")

    plt.title(title)
    plt.show()


#Plot Datapoints
plot(False, False, "Random Datapoints")


def euclidean_distance(data_point_a, data_point_b): #calculates euclidean distance
    x_a = data_point_a[0]
    y_a = data_point_a[1]
    z_a = data_point_a[2]
    x_b = data_point_b[0]
    y_b = data_point_b[1]
    z_b = data_point_b[2]
    
    eucl_dist = round(math.sqrt((x_a - x_b) ** 2 + (y_a - y_b) ** 2 + (z_a - z_b) ** 2),2)
    
    return eucl_dist

def selectRandomCenters(k): # returns k random data points from all data points E
    return random.sample(E, k)


# Choose random datapoints as starting cluster centers
C = selectRandomCenters(k)
plot(True, False, "Choose {} random cluster-centers".format(k))


def argminDistance(e): # calculates closest cluster for a given datapoint
    minDist = 100

    for c in C:
        dist = euclidean_distance(e,c)
        if dist < minDist:
            minDist = dist
            minDistCenter = c
            
    return C.index(minDistCenter)


# Find closest cluster for each datapoint

for e in E:
    L[e] = argminDistance(e)

print("Labels:")

for l in L:
    print("Point",l,", closest cluster-center:",L[l],"at",C[L[l]],", distance:",euclidean_distance(l,C[L[l]]))

plot(True, True, "Assign datapoints to closest cluster-center")


def UpdateCluster(c): # moves given cluster to mean position of its current corresponding datapoints
    print("Updating cluster",C.index(c)," at ",c," ...")
    pts = []

    for l in L:
        if (C[L[l]]) == c:
            pts.append(l)

    sumX = 0
    sumY = 0
    sumZ = 0

    for x,y,z in pts:
        sumX += x
        sumY += y
        sumZ += z
    
    newPos = (round(sumX/len(pts),0),round(sumY/len(pts),0),round(sumZ/len(pts),0))

    if newPos == c:
        print("Cluster-center-position ",C.index(c)," is already optimal")
    else:
        print("Cluster-center ",C.index(c)," moved to ",newPos)

    print("")

    return newPos


# optimize cluster-positions
iter = 0
maxIters = 100

print("Optimizing cluster-center-positions ...")

while True:
    print(" ")
    print("Iteration ",iter + 1)
    print(" ")
    changed = False

    # Update clusters
    for i,c in enumerate(C):
        C[i] = UpdateCluster(c)

    # Update minDist
    print("Distance from points to cluster-centers that changed:")
    for e in E:
        minDist = euclidean_distance(e,C[argminDistance(e)])

        if minDist != euclidean_distance(e,C[L[e]]):
            L[e] = argminDistance(e)
            print("Distance from point",e,"to cluster",C[L[e]],"changed to",euclidean_distance(e,C[L[e]]))
            changed = True

    if not changed:
        print("None")

    iter += 1

    if not changed or iter > maxIters:
        break

print(" ")
print("Optimization done")
print("Number of iterations needed: ",iter)
plot(True, True, "Optimize cluster-center-positions")
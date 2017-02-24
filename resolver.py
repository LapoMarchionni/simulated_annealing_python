from problems import NQueensProblem, MagicSquaresProblem, TravellingSalesmanProblem
from simulated_annealing import simulated_annealing
from numpy import sum as npsum
import timeit, sys

def resolve_problems(problem, iterations, solution=False):
    error = 0
    times = []
    path_cost = []
    routes = []
    init = timeit.default_timer()
    print(problem.name, "problem")
    print("Temperature: %s. Max iterations: %s" %(problem.temperature, problem.temperature*10))
    for x in range(iterations):
        start = timeit.default_timer()
        result = simulated_annealing(problem)
        stop = timeit.default_timer()
        print(x)
        times.append(stop-start)
        if problem.name == 'N-Queens':
            error += 1 if len(set(result.state)) != problem.N else 0
        if problem.name == 'Travelling Salesman':
            routes.append(problem.value(result.state))
        if problem.name == 'Magic Square':
            error += 1 if problem.value(result.state) != 0 else 0
        path_cost.append(result.path_cost)
        if solution:
            print(result.state)
    avgt = npsum(times)/len(times)
    avgpc = 0
    if len(path_cost) != 0:
        avgpc = npsum(path_cost)/len(path_cost)
    if len(routes) != 0:
        avgroute = npsum(routes)/len(routes)
        print("Average best route lenght %skm" % (int(avgroute)))
    print("Done in %ss. with average time of %ss per problem and an average cost of %i" % (round(float(stop-init), 3), round(avgt,3), int(avgpc)))
    print("Errors", error)

if __name__ == "__main__":
    cities_world = {
        "Buenos Aires, Argentina": (-34.603684, -58.381559),
        "Sydney, Australia": (-33.868820, 151.209296),
        "Rio de Janeiro, Brazil": (-22.906847, -43.172896),
        "Montreal, Canada": (45.501689, -73.567256),
        "Beijing, China": (39.904211, 116.407395),
        "Moroni, Comoros": (-11.717216, 43.247315),
        "Cairo, Egypt": (30.044420, 31.235712),
        "Paris, France": (48.856614, 2.352222),
        "Athens, Greece": (37.983810, 23.727539),
        "Budapest, Hungary": (47.497912, 19.040235),
        "Reykjavik, Iceland": (64.126521, -21.817439),
        "Delhi, India": (28.704059, 77.102490),
        "Baghdad, Iraq": (33.312806, 44.361488),
        "Rome, Italy": (41.902783, 12.496366),
        "Tokyo, Japan": (35.689487, 139.691706),
        "Bamako, Mali": (12.639232, -8.002889),
        "Mexico City, Mexico": (19.432608, -99.133208),
        "Kathmandu, Nepal": (27.717245, 85.323960),
        "Oslo, Norway": (59.913869, 10.752245),
        "Port Moresby, Papua New Guinea": (-9.478012, 147.150654),
        "Lima, Peru": (-12.046374, -77.042793),
        "Kigali, Rwanda": (-1.970579, 30.104429),
        "Singapore, Singapore": (1.352083, 103.819836),
        "Moscow, Russia": (55.755826, 37.617300),
        "Colombo, Sri Lanka": (6.927079, 79.861243),
        "Bangkok, Thailand": (13.756331, 100.501765),
        "Istanbul, Turkey": (41.008238, 28.978359),
        "London, UK": (51.507351, -0.127758),
        "New York, USA": (40.712784, -74.005941)
    }


    sys.stdout.write("Choose a problem: \n\t1. N-Queens\n\t2. Travelling Salesman \n\t3. Magic Squares\n")
    choice = input().lower()
    if choice == '1':
        sys.stdout.write("Choose the dimension [NxN with N queens]: ")
        N = int(input().lower())
        sys.stdout.write("Choose the starting temperature: ")
        temp = int(input().lower())
        resolve_problems(NQueensProblem(N, temp), 100, False)
    if choice == '2':
        sys.stdout.write("Choose the starting temperature: ")
        temp = int(input().lower())
        resolve_problems(TravellingSalesmanProblem(cities_world, temp), 100, False)
    if choice == '3':
        sys.stdout.write("Choose the dimension [NxN matrix]: ")
        N = int(input().lower())
        sys.stdout.write("Choose the starting temperature: ")
        temp = int(input().lower())
        resolve_problems(MagicSquaresProblem(N, temp), 100, False)
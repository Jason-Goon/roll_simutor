import random
import multiprocessing
import time


def simulate_events(trials):
    any_two_same_twice_count = 0
    predefined_same_twice_count = 0
    predefined_exact_count = 0
    any_two_exact_count = 0

    for _ in range(trials):
        first_round = [random.randint(1, 100) for _ in range(9)]

        for i in range(9):
            for j in range(i+1, 9):
                if first_round[i] == first_round[j] and first_round.count(first_round[i]) == 2:
                    second_round_person1 = random.randint(1, 100)
                    second_round_person2 = random.randint(1, 100)
                    if second_round_person1 == second_round_person2:
                        any_two_same_twice_count += 1
    

        if first_round[0] == first_round[1] and first_round.count(first_round[0]) == 2:
            second_round_person1 = random.randint(1, 100)
            second_round_person2 = random.randint(1, 100)
            if second_round_person1 == second_round_person2:
                predefined_same_twice_count += 1

        if first_round[0] == 99 and first_round[1] == 99 and first_round.count(99) == 2:
            second_round_person1 = random.randint(1, 100)
            second_round_person2 = random.randint(1, 100)
            if second_round_person1 == 6 and second_round_person2 == 6:
                predefined_exact_count += 1

       
        for i in range(9):
            for j in range(i+1, 9):
                if first_round[i] == 99 and first_round[j] == 99 and first_round.count(99) == 2:
                    second_round_person1 = random.randint(1, 100)
                    second_round_person2 = random.randint(1, 100)
                    if second_round_person1 == 6 and second_round_person2 == 6:
                        any_two_exact_count += 1

    return {
        "any_two_same_twice": any_two_same_twice_count,
        "predefined_same_twice": predefined_same_twice_count,
        "predefined_exact": predefined_exact_count,
        "any_two_exact": any_two_exact_count,
        "trials": trials
    }

def run_parallel_simulations(total_trials, batch_size):
    num_batches = total_trials // batch_size
    pool = multiprocessing.Pool()
    trials_per_batch = [batch_size] * num_batches

    remaining_trials = total_trials % batch_size
    if remaining_trials > 0:
        trials_per_batch.append(remaining_trials)
        num_batches += 1


    start_time = time.time()
    results_list = []
    for idx, result in enumerate(pool.imap_unordered(simulate_events, trials_per_batch), 1):
        results_list.append(result)
        # Periodically print progress
        if idx % 1 == 0: 
            elapsed_time = time.time() - start_time
            print(f"Completed batch {idx}/{num_batches} - Elapsed time: {elapsed_time:.2f} seconds")

    pool.close()
    pool.join()

    # Aggregate results
    final_results = {
        "any_two_same_twice": 0,
        "predefined_same_twice": 0,
        "predefined_exact": 0,
        "any_two_exact": 0,
        "trials": 0
    }
    for batch_results in results_list:
        for key in final_results:
            final_results[key] += batch_results[key]

    return final_results


if __name__ == '__main__':
    total_trials = 1000000000 
    batch_size = 1000000    

    # Run the simulation
    results = run_parallel_simulations(total_trials=total_trials, batch_size=batch_size)

    # Calculate probabilities
    probability_any_two_same_twice = results['any_two_same_twice'] / results['trials']
    probability_predefined_same_twice = results['predefined_same_twice'] / results['trials']
    probability_predefined_exact = results['predefined_exact'] / results['trials']
    probability_any_two_exact = results['any_two_exact'] / results['trials']

    # Print the results
    print("\nFinal Results:")
    print(f"Total Trials: {results['trials']}")
    print(f"Any two people rolling the same number twice: {results['any_two_same_twice']} occurrences")
    print(f"Probability: {probability_any_two_same_twice:.8f}")

    print(f"\nPredefined two people rolling the same number twice: {results['predefined_same_twice']} occurrences")
    print(f"Probability: {probability_predefined_same_twice:.8f}")

    print(f"\nPredefined two people rolling 99 first and 6 second: {results['predefined_exact']} occurrences")
    print(f"Probability: {probability_predefined_exact:.8f}")

    print(f"\nAny two people rolling 99 first and 6 second: {results['any_two_exact']} occurrences")
    print(f"Probability: {probability_any_two_exact:.8f}")

    # Write results to a file
    with open('simulation_results.txt', 'w') as file:
        file.write(f"Simulation Results:\n")
        file.write(f"Total Trials: {results['trials']}\n")
        file.write(f"Any two people rolling the same number twice: {results['any_two_same_twice']} occurrences\n")
        file.write(f"Probability: {probability_any_two_same_twice:.8f}\n\n")

        file.write(f"Predefined two people rolling the same number twice: {results['predefined_same_twice']} occurrences\n")
        file.write(f"Probability: {probability_predefined_same_twice:.8f}\n\n")

        file.write(f"Predefined two people rolling 99 first and 6 second: {results['predefined_exact']} occurrences\n")
        file.write(f"Probability: {probability_predefined_exact:.8f}\n\n")

        file.write(f"Any two people rolling 99 first and 6 second: {results['any_two_exact']} occurrences\n")
        file.write(f"Probability: {probability_any_two_exact:.8f}\n")

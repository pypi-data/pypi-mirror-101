from .star import star
import pathos.multiprocessing as mp

class Formation:
    # Contains multiple stars; Chains them and run them.
    def __init__(self, star=None):
        self.head = star
        self.end = star

    def add(self, s: star):
        # Add first star in formation or chain stars to the last added star.
        if self.head is None:
            self.head = s
            self.end = s
        else:
            self.end.link(s)
            self.end = s

    def mp_run(self, input, cores):
        # run all process on multi-processes and save output
        def run_star(star, input):
            # Run all the star and save output of last stars
            output = star.action(input)
            return output

        stars = [(self.head, input)]
        while len(stars):
            with mp.Pool(cores) as p:
                outputs = p.starmap(run_star, [(i, input) for i, input in stars])
                next_stars = []
                for outputNum, (star, _) in enumerate(stars):
                    next_stars += zip(star._nodes, [outputs[outputNum]] * len(star._nodes))
                stars = next_stars
        return outputs

    def run(self, input = None, multicpu:int = 0):
        if multicpu > 1:
            return self.mp_run(input, multicpu)
        # run all star actions and return output
        outputs=[]

        def run_star(star, input):
            # Run all the star and save output of last stars
            output = star.action(input)
            for i in star._nodes:
                run_star(i, output)
            if len(star._nodes) == 0:
                outputs.append(output)

        run_star(self.head, input)
        return outputs

class formation:
    # Contains multiple stars
    def __init__(self, star=None):
        self.head = star
        self.end = star

    def add(self, star):
        # add stars
        if self.head is None:
            self.head = star
            self.end = star
        else:
            self.end._nodes.append(star)
            self.end=star

    def run(self, input=None):
        # run all star actions and return output
        outputs=[]

        def run_star(star, input):
            # Run all the star and save output of last stars
            output = star.action(input)
            for i in star._nodes:
                run_star(i, output)
            if len(star._nodes)==0:
                outputs.append(output)
        run_star(self.head, input)
        return outputs

import BeamType as bt
import matplotlib.pyplot as plt

if __name__ == "__main__":
    beam_list = bt.get_beam_list()
    print("welcome to Beam Diffraction Visualizer")

    while 1:
        beamtype = input("Select beam type (-1: exit, 0: basic, 1: gaussian, 2: laguerre-gaussian): ").strip().lower()
        print("")
        if beamtype == "-1" or beamtype == "exit":
            break
        elif (beamtype in beam_list) or (beamtype in [str(i) for i in range(len(beam_list))]):
            if beamtype == "basic" or beamtype == "0":
                Beam = bt.Beam()
            elif beamtype == "gaussian" or beamtype == "1":
                Beam = bt.Gaussian_Beam()
            elif beamtype == "laguerre-gaussian" or beamtype == "2":
                Beam = bt.Laguerre_Gaussian_Beam()
        else:
            print("Invalid input. Please select a valid beam type.")
            continue

        temp = "n"
        while temp != "y" and temp != "yes":
            temp = input("Use default variables? (y/n): ").strip().lower()
            if temp == "n" or temp == "no":
                Beam.get_var()
                break
        Beam.list()
        print("Generating beam profile...")
        Beam.plot_beam()
        print("Generation complete.(please close the plot window to continue)\n")
        plt.show()

    print("Exiting Beam Diffraction Visualizer.")
    print("Thanks for using!")
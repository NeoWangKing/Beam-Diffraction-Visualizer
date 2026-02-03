import Beam as bt
import Aperture as ap
import Diffraction as df
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":
    beam_list = bt.get_beam_list()
    print("welcome to Beam Diffraction Visualizer")

    while 1:
        beamtype = input("Select beam type (-1: exit, 0: basic, 1: gaussian, 2: laguerre-gaussian): ").strip().lower()
        print("")
        if beamtype == "-1" or beamtype == "exit":
            sys.exit(0)
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
        Beam.list()
        while temp != "y" and temp != "yes":
            temp = input("Use default variables? (y/n): ").strip().lower()
            print("")
            if temp == "n" or temp == "no":
                for name in Beam.__dict__:
                    if name != "beamtype" and name != "lam" and name != "plotrange" and name != "resolution":
                        Beam.__dict__[name][0] = eval(input(f"Enter value for {name} (current value: {Beam.__dict__[name][0]} {Beam.__dict__[name][2]}): "))
                    elif name == "lam":
                        Beam.__dict__[name][0] = eval(input(f"Enter value for lam(nm) (current value: {Beam.__dict__[name][0] * 1e9} {Beam.__dict__[name][2]}): ")) * 1e-9
                    elif name == "plotrange":
                        plotrange = Beam.__dict__[name][0] = eval(input(f"Enter value for {name} (current value: {Beam.__dict__[name][0]} {Beam.__dict__[name][2]}): "))
                    elif name == "resolution":
                        resolution = Beam.__dict__[name][0] = eval(input(f"Enter value for {name} (current value: {Beam.__dict__[name][0]} {Beam.__dict__[name][2]}): "))
                    else:
                        pass
                print("Variables updated.\n")
                #Beam.list()
                break

        while 1:
            aperturetype = input("Select aperture type (-1:exit, 0: circular, 1: rectangular, 2: fresnel half-wave zone): ").strip().lower()
            print("")
            if aperturetype == "-1" or aperturetype == "exit":
                sys.exit(0)
            elif aperturetype == "circular" or aperturetype == "0":
                Aperture = ap.Circular_Aperture()
            elif aperturetype == "rectangular" or aperturetype == "1":
                Aperture = ap.Rectangular_Aperture()
            elif aperturetype == "fresnel half-wave zone" or aperturetype == "2":
                Aperture = ap.Fresnel_Half_Wave_Zone_Aperture()
            else:
                print("Invalid input. Please select a valid aperture type.")
                continue
        
            temp = "n"
            Aperture.list()
            while temp != "y" and temp != "yes":
                temp = input("Use default variables? (y/n): ").strip().lower()
                if temp == "n" or temp == "no":
                    for name in Aperture.__dict__:
                        if name != "aperturetype" and name != "plotrange" and name != "resolution":
                            Aperture.__dict__[name][0] = eval(input(f"Enter value for {name} (current value: {Aperture.__dict__[name][0]} {Aperture.__dict__[name][2]}): "))
                        elif name == "plotrange":
                            Aperture.__dict__[name][0] = plotrange
                        elif name == "resolution":
                            Aperture.__dict__[name][0] = resolution
                        else:
                            pass
                    print("Variables updated.\n")
                    #Aperture.list()
                    break

            distance = eval(input("Enter propagation distance for diffraction (m): "))
            print("Variables Updated.\n")

            Beam.list()
            Aperture.list()
            print("Diffraction Parameters:")
            print(f"{'Parameter':<25}{'Variable':<15}{'Value':<10}{'Unit'}")
            print(f"{'Propagation distance':<25}{distance:<15}{distance:<10}{'m'}\n")

            diffraction = df.Diffraction(input_beam=Beam, aperture=Aperture, distance=distance)

            plt.subplot(2, 3, 1)
            Beam.plot_intensity()
            plt.subplot(2, 3, 2)
            Beam.plot_phase()
            plt.subplot(2, 3, 3)
            Aperture.plot_aperture()
            plt.subplot(2, 3, 4)
            diffraction.plot_diffraction_intensity()
            plt.subplot(2, 3, 5)
            diffraction.plot_diffraction_phase()
            plt.subplot(2, 3, 6)
            plt.axis('off')
            plt.suptitle("Beam Diffraction through Aperture")
            
            print("Displaying summary plot.(please close the plot window to continue)\n")
            plt.show()
            break


    print("Exiting Beam Diffraction Visualizer.")
    print("Thanks for using!")
import h5py

with h5py.File("truthmark_artifacts/classifier_weights_final.weights.h5", "r") as hf:
    def walk(name, obj):
        print(name)
    hf.visititems(walk)

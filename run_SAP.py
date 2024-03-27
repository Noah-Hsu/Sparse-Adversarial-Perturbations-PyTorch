import subprocess


subprocess.run(["D:\\APPS\\AnaConda\\envs\\anaconda\\python", "l21_optimization.py",
                "--input_dir", "../../0Dataset/UCF101/UCF-101-frames",
                "--split_path", "../../0Dataset/UCF101/ucfTrainTestlist",
                "--checkpoint_model", "ConvLSTM_150.pth"])

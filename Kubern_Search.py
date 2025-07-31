import subprocess
import os
import sys


def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True)
    
    # Attempt to decode the output, handle potential UnicodeDecodeError
    try:
        output = result.stdout.decode('utf-8-sig').strip()
    except UnicodeDecodeError:
        try:
            output = result.stdout.decode('utf-8-sig').strip()  # Use a different encoding
        except Exception as e:
            output = f"Error decoding output: {e}"
    
    return output, result.returncode

def find(path, n, Type_recorded_file ,Date = None,dest_sourcd=None ,pod=None, namespace='namespace'):
    Types = ["sms","rec","data","com","mon","mgr","vou","clr"]
    if Date:
        BakFinder = f"kubectl exec -n {namespace} {pod} -- find {path}/backup/filecleanerbak/ -name '*{Date}*'"
        output,return_code = run_command(BakFinder)
        if return_code == 0:
            directories = [path.split("/")[-1] for path in output.split("\n")]  # Extract filenames
        
            if pod:
                if Type_recorded_file in Types :
                    grep_command = f"kubectl exec -n {namespace} {pod} -- find {path}/backup/filecleanerbak/{directories[0]}/ -name '*{Type_recorded_file}*' -exec zgrep -l {n} {{}} +"
                else:
                    grep_command = f"grep -rl {n} {path}"

                output, return_code = run_command(grep_command)

            if return_code == 0:
                save_file_source = []
                for file in output.splitlines():  
                    full_path = os.path.join(path, file)  
                    save_file_source.append(full_path)
                    if pod and dest_sourcd:
                        copy_command = f"kubectl cp {namespace}/{pod}:{full_path} {dest_sourcd}/{os.path.basename(file)}"
                        run_command(copy_command)
                        print(f"recorded_file is finded here {pod}")
                    elif pod and not dest_sourcd:
                        dest_sourcd = "/tmp/recorded_file/"
                        copy_command = f"kubectl cp {namespace}/{pod}:{full_path} /tmp/recorded_file/{os.path.basename(file)}"
                        run_command(copy_command)
                        print(f"recorded_file is finded here {pod}")
                    else:
                        print(f"Local copy: {full_path} to /tmp/recorded_file/{os.path.basename(file)}")
                return save_file_source 
    else:
        if pod:
            if Type_recorded_file in Types:
                grep_command = f"kubectl exec -n {namespace} {pod} -- find {path} -name '*{Type_recorded_file}*' -exec grep -rl {n} {{}} +"
        else:
            grep_command = f"grep -rl {n} {path}"

        output, return_code = run_command(grep_command)

        if output:
            save_file_source = []
            for file in output.splitlines():  
                full_path = os.path.join(path, file)  
                save_file_source.append(full_path)
                if pod and dest_sourcd:
                    copy_command = f"kubectl cp {namespace}/{pod}:{full_path} {dest_sourcd}/{os.path.basename(file)}"
                    run_command(copy_command)
                    print(f"recorded_file is finded here {pod}")
                elif pod and not dest_sourcd:
                    dest_sourcd = "/tmp/recorded_file/"
                    copy_command = f"kubectl cp {namespace}/{pod}:{full_path} /tmp/recorded_file/{os.path.basename(file)}"
                    run_command(copy_command)
                    print(f"recorded_file is finded here {pod}")
                else:
                    print(f"Local copy: {full_path} to /tmp/recorded_file/{os.path.basename(file)}")
            return save_file_source  

def download(path = None,Date =None):
    """Zip the files in /tmp/recorded_file and download the zip file using sz."""
    default_zip_file_path = "/tmp/recorded_file"
    
    NStore_Path = path

    if not NStore_Path:
        NStore_Path = default_zip_file_path
    if Date:
        print("Not Allowed download .gz file")
        sys.exit()
    
    run_command(f"zip -r {NStore_Path}.zip {NStore_Path}*")
    
    user_input = input(f"Y to download {NStore_Path}.zip, N denied: ").strip().upper()
    
    if user_input == 'Y':
        run_command(f"chmod 777 {NStore_Path}.zip")
        if os.path.exists(NStore_Path):
            subprocess.run(['sz', f"{NStore_Path}.zip"], check=True)
            print(f"File '{NStore_Path}' sent successfully.")
        else:
            print(f"File {NStore_Path} does not exist.")
    elif user_input == 'N':
        print("Download denied.")
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")

def main():
    Date1 = input('Please Enter Date example 20250101 (If is today just Enter ): ')
    Type_recorded_file = input("Enter recorded_file Type: ").strip().lower()
    Pod_Number = int(input("Put Number for pod1 = 0 , pod2 = 1 , pod3 = 2 , pod4 = 3 , pod5 = 4: "))
    Payment_Mode = input("Enter pps/pos: ").strip().lower()
    Number1 = input("Enter Number: ")
    Dest_Source = None 
    recorded_file_Mode = None
    tempFinder = "N"
    if Date1.strip() == "":
        tempFinder = input("Do you want just check temp? (Y/N)").strip().upper()
    Checking = input ("For fail recorded_file Please write fail وOtherwise just enter: ").strip().lower()
    if Checking:
        recorded_file_Mode = Checking
    else:
        recorded_file_Mode = "normal"
    Dest_Check = input("Enter Path for Saving: (exp /tmp/X) ").strip()
    if Dest_Check:
        Dest_Source = Dest_Check
    
    podName = ["pod1","pod2","pod3","pod4","pod5"]
    if tempFinder == 'Y':
        pathrecorded_file = f"/onip/recorded_file/{podName[Pod_Number]}/output/{Payment_Mode}/{recorded_file_Mode}/temp"
    elif tempFinder == 'N':
        pathrecorded_file = f"/onip/recorded_file/{podName[Pod_Number]}/output/{Payment_Mode}/{recorded_file_Mode}"
    else:
        print("Wrong Charater")
    
    first_run_command = f"kubectl get pod -owide -n namespace | grep -v Completed | grep {podName[Pod_Number]}"
    
    output, return_code = run_command(first_run_command)
    if return_code != 0:
        print("No running pods found.")
        return
    
    array_x = [line.split()[0] for line in output.splitlines()]
    print (f"There are {len(array_x)} pod\n")
    all_copied_files = []  

    for pod in array_x:
        if Payment_Mode in ['pps', 'pos']:
            save_file_source = find(pathrecorded_file, Number1, Type_recorded_file,Date1,Dest_Source,pod)
            if save_file_source:
                all_copied_files.extend(save_file_source)
        else:
            print("Wrong Path")
    if len(all_copied_files) == 0:
        print("No File found")
        sys.exit()
    else:
        if all_copied_files:
            if Dest_Source:
                download(Dest_Source,Date1)
            else:
                download()
        else:
            print("No files to download.")

if __name__ == "__main__":
    main()

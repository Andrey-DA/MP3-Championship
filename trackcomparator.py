from pynput import keyboard
import time

class TrackComparator:
    def __init__(self):
        self.choice = None
        self.running = True

    def on_press(self, key):
        try:
            # Check for pressing numbers
            if key.char in ['1', '2', '3', '4']:
                self.choice = int(key.char)
                self.running = False
                return False  # stop listener
        except AttributeError:
            pass

    def show_menu(self):
        print("\n" + "="*50)
        print("Estimate tracks:")
        print("1 - First track is better")
        print("2 - Second track is better")
        print("3 - Tie")
        print("4 - Listen one more time...")
        print("="*50)
        print("Press button 1, 2, 3 or 4...")

    def get_user_choice(self):
        self.choice = None
        self.running = True
        
        self.show_menu()
        
        # Start listening keyboard...
        with keyboard.Listener(on_press=self.on_press) as listener:
            while self.running:
                time.sleep(0.1)  # Little pause
            
            listener.stop()
        
        return self.choice

    def process_choice(self, choice):
        """Processing operator choice"""
        if choice == 1:
            print("\nFirst track won...")
        elif choice == 2:
            print("\nSecond track won...")
        elif choice == 3:
            print("\nTie...")
        elif choice == 4:
            print("\nListening one more time...")
            return True  
        else:
            print("\nWrong input!")
            return False
        
        return False  
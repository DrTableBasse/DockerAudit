from dockerauditagent.rootless import check_docker_rootless

def display_menu():
    print("\nMenu de vérification Docker:")
    print("1. Vérifier si Docker fonctionne en mode rootless")
    print("2. Quitter")

def main():
    while True:
        display_menu()  # Affiche le menu
        choice = input("Choisissez une option (1 ou 2): ")

        if choice == '1':
            print("Vérification du mode rootless de Docker...\n")
            check_docker_rootless()  # Appel de la fonction pour vérifier le mode rootless
        elif choice == '2':
            print("Au revoir!")
            break  # Quitter le programme
        else:
            print("Choix invalide. Veuillez entrer 1 ou 2.")

if __name__ == "__main__":
    main()

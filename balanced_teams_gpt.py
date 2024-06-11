import pandas as pd
import numpy as np

NAME = 'Dati anagrafici bambino/a'
SEX = 'Sesso'
AGE = 'Classe frequentata'
WEEK1 = 'Giornata (1^settimana)'
WEEK2 = 'Giornata (2^settimana)'
WEEK3 = 'Giornata (3^settimana)'
FULL = 'Intera (60€)'
AM_ONLY = 'Solo mattina (35€)'


def mask_pm_only(df):
    mask = np.logical_or(np.logical_or(np.logical_or(df[WEEK1] == FULL, df[WEEK1] == AM_ONLY),
                                       df[WEEK2] == FULL, df[WEEK2] == AM_ONLY),
                                       df[WEEK3] == FULL, df[WEEK3] == AM_ONLY)
    return df[mask]


def sort_dataframe(df):
    return df.sort_values(by=[AGE, SEX, WEEK1, WEEK2, WEEK3], ascending=False)


def distribute_participants(participants, n_teams=4):
    # Initialize teams
    teams = [[] for _ in range(n_teams)]

    # Distribute participants into teams
    for i, participant in enumerate(participants.iterrows()):
        teams[i % n_teams].append(participant[1])

    return teams


def print_team_stats(teams):
    for i, team in enumerate(teams):
        print(f"\nSquadra {i + 1} ({len(team)} partecipanti)")
        week1_count = sum(1 for member in team if member[WEEK1] in [FULL, AM_ONLY])
        week2_count = sum(1 for member in team if member[WEEK2] in [FULL, AM_ONLY])
        week3_count = sum(1 for member in team if member[WEEK3] in [FULL, AM_ONLY])
        print(f"Numero di membri per 1^ settimana: {week1_count}")
        print(f"Numero di membri per 2^ settimana: {week2_count}")
        print(f"Numero di membri per 3^ settimana: {week3_count}")
        for member in team:
            print(f"{member[NAME]} - {member[AGE]} - {member[SEX]} - {member[WEEK1]} - {member[WEEK2]} - {member[WEEK3]}")
            # Print the index of the member
            row_label = member.name
            row_index = df.index.get_loc(row_label)
            print(f"Index of the row: {row_index}")


def main():
    file_path = 'teams.csv'
    df = pd.read_csv(file_path, delimiter=',', index_col=None, header=0)
    df.set_index(NAME, inplace=True)

    participants = mask_pm_only(df)

    participants = sort_dataframe(participants)

    # Distribute participants into initial teams
    teams = distribute_participants(participants)

    print_team_stats(teams)


if __name__ == "__main__":
    main()

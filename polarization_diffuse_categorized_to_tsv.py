import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("polarization_diffuse_categorized.tsv", sep='\t')

    rows = []
    for curie, name, pol, dif, pol_all, dif_all, zeta in df.values:
        curie = curie.strip()
        name = name.strip()
        if pol_all:
            rows.append((curie, name, "BSEO:0100070", "basis set with polarization function for all atoms"))
        elif pol:
            rows.append(
                (curie, name, "BSEO:0100081", "basis set with polarization function for some but not all atoms"))

        if dif_all:
            rows.append((curie, name, "BSEO:0100068", "basis set with diffusion function for all atoms"))
        elif dif:
            rows.append((curie, name, "BSEO:0100080", "basis set with diffusion function for some but not all atoms"))

        if pd.isna(zeta):
            pass
        elif zeta == "double":
            rows.append((curie, name, "BSEO:0100073", "basis set with double zeta (DZ)"))
        elif zeta == "triple":
            rows.append((curie, name, "BSEO:0100074", "basis set with triple zeta (TZ)"))
        else:
            raise ValueError(zeta)

    df_target = pd.read_csv("templates/basis-set-parents.tsv", sep='\t')
    df_target = pd.concat([df_target, pd.DataFrame(rows)])
    df_target.to_csv("templates/basis-set-parents.tsv", sep='\t', index=False)

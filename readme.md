The repository hereby provides an automatic process of translation form the PIPER metadata to the LSTC metadata required to use the dummy positioning tool in pre-processor environments such as Altair Hypermesh and LS-Prepost.

The first draft of the repo uses the VIVA+ v2 human body model (HBM).

The repository is under construction, just a first version has been implemented. The main issue that occur during the translation process are the following:
- Piper works for joint movements, with slave and master entities. LSTC works for limb movements, with children and parents elements. If a PIPER entity is a slave in more than one joint, this entity cannot be recalled as limb with more than one parent.
- Soft tissues in piper are explicitely stated. In LSTC, the soft tissues parts must stay in the limb. This diversity in definitions does not allow fully automatic translation at the moment.
- The LSTC human definition requires a base limb which is fixed, which is not the case of PIPER.

Further work will be brought on the next months.
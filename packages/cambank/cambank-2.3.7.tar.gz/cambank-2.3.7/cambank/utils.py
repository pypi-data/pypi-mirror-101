# cette fonction prend la liste complete des operations, la trie afin de pouvoir
# filtrer les operations deja traitees et enrichir les operations en attente
# avec la liste des operations similaire
# but : montrer les doublons
def filter_pending_operations(ops):
  ops = sorted(ops, key = lambda x: (x.odate, abs(x.omontant), abs(x.obalance)))
  oplist = []
  curop = None
  while len(ops) > 0:
    newop = ops.pop(0)
    if curop == None:
      if newop.obalance != newop.omontant:
        curop = newop
      continue
    # we have curop and newop
    # --
    # first, if new is same than cur, we enrich cur and skip new
    if curop.odate == newop.odate and \
       curop.omontant == newop.omontant:
      if 'similar' not in curop.__dict__:
        curop.similar = []
      curop.similar.append(newop)
    # and if already processed, we skip it as being cur itself
    if newop.obalance == newop.omontant:
      continue
    oplist.append(curop)
    curop = newop
  if curop is not None:
    oplist.append(curop)
  return oplist


class Op:
  def __init__(self, odate, omontant, obalance):
    self.odate = odate
    self.omontant = omontant
    self.obalance = obalance
  def __repr__(self):
    return '({}, {}, {})'.format(self.odate, self.omontant, self.obalance)

def test_filter_pending_operations():
  h1 = [
    Op(1, 1, 0),
    Op(2, 1, 1),
    Op(3, 1, 0),
    Op(3, 1, 0),
  ]
  h2 = filter_pending_operations(h1)
  assert len(h2) == 3
  assert h2[2] in h2[1].similar

if __name__ == '__main__':
  test_filter_pending_operations()

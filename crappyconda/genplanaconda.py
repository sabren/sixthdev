
import workshop


_goal = workshop.ProtoClass(name="Goal")
_goal.attrs << workshop.ProtoAttr(name="ID", type="long")
_goal.attrs << workshop.ProtoAttr(name="name", type="str")
_goal.attrs << workshop.ProtoAttr(name="note", type="str")

_model = workshop.Model()
_model.add(_goal)

out = open("_planaconda.py", "w")
print >> out, _model.asCode()
out.close()


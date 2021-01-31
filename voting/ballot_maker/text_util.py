
def get_choice_string(choice_num):
  if choice_num == 1:
    suffix = "st"
  elif choice_num == 2:
    suffix = "nd"
  elif choice_num == 3:
    suffix = "rd"
  else:
    suffix = "th"
  return str(choice_num) + suffix

def get_choice_num_as_word(choice_num):
  order = { 1: "first",
            2: "second",
            3: "third",
            4: "fourth",
            5: "fifth",
            6: "sixth",
            7: "seventh",
            8: "eighth",
            9: "ninth" }
  return order.get(choice_num, "%dth" % choice_num)


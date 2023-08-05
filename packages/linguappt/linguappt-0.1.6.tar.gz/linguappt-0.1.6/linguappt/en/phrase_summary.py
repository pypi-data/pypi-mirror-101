from linguappt.phrase_ppt import PhrasePPT
import os
import json

class EnglishPhrasePPT(PhrasePPT):
  """Create Phrase PPT for English study

  Attributes:
    content (list of dict): read from csv file
  """

  _template_dir = os.path.dirname(__file__)
  _templates = {
    "classic": os.path.join(_template_dir, 'templates/phrase_english_classic.pptx'),
  }
  lang = 'en'

  content_keys = ["sentence", "noun_phrases", "prep_phrases", "verb_phrases", "verbs"]

  def __init__(self, sourcefile, title="", genre="classic"):
    super().__init__(sourcefile, title, genre)

  def _create_three_kinds_phrase(self, line):
    sentence_obj = json.loads(line["sentence"])
    nps_obj = json.loads(line["noun_phrases"])[:3]
    pps_obj = json.loads(line["prep_phrases"])[:3]
    #vps_obj = json.loads(line["verb_phrases"])[:3]

    layout = self._prs.slide_layouts.get_by_name("Three kinds of phrase")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders
  
    st_holder, sm_holder = holders[10], holders[11]
    st_holder.text_frame.text = sentence_obj["text"]
    sm_holder.text_frame.text = sentence_obj["meaning"]

    for index, np in enumerate(nps_obj):
      base_index = 12 + index*2

      t_holder, m_holder = holders[base_index], holders[base_index+1]
      t_holder.text_frame.text = np["text"]
      m_holder.text_frame.text = np["meaning"]

    for index, pp in enumerate(pps_obj):
      base_index = 18 + index*2

      t_holder, m_holder = holders[base_index], holders[base_index+1]
      t_holder.text_frame.text = pp["text"]
      m_holder.text_frame.text = pp["meaning"]

    #for index, vp in enumerate(vps_obj):
    #  t_holder, m_holder = holders[24+index], holders[25+index]
    #  t_holder.text_frame.text = vp["text"]
    #  m_holder.text_frame.text = vp["meaning"]

  def _create_phrase_and_verb(self, line):
    sentence_obj = json.loads(line["sentence"])
    nps_obj = json.loads(line["noun_phrases"])[:2]
    pps_obj = json.loads(line["prep_phrases"])[:2]
    ps_obj = nps_obj + pps_obj
    vs_obj = json.loads(line["verbs"])[:4]

    layout = self._prs.slide_layouts.get_by_name("Phrase and verb")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders
  
    st_holder, sm_holder = holders[10], holders[11]
    st_holder.text_frame.text = sentence_obj["text"]
    sm_holder.text_frame.text = sentence_obj["meaning"]

    for index, p in enumerate(ps_obj):
      base_index = 12 + index*2

      t_holder, m_holder = holders[base_index], holders[base_index+1]
      t_holder.text_frame.text = p["text"]
      m_holder.text_frame.text = p["meaning"]

    for index, v in enumerate(vs_obj):
      base_index = 20+index*3
      verb_holder, origin_holder, form_holder = holders[base_index], holders[base_index+1], holders[base_index+2]

      verb_holder.text_frame.text = v["text"]
      origin_holder.text_frame.text = v["lemma"]
      form_holder.text_frame.text = v["form"].split(",")[1]
 
  def _create_phrase(self):
    """Create phrase by sentence, which are noun phrases, prep phrases, verb phrases
    """
    for line in self.content:
      self._create_phrase_and_verb(line)



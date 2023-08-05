import os
import tempfile
import unittest

import src.coh_piggs_extractor.coh_piggs_extractor

expected_extracted_files = {'depts.bin', 'bodyparts.bin', 'arenamaps.bin', 'boost_effect_below.bin',
                            'proficiencyids.bin', 'pc_def_objects.bin', 'pc_def_sequencer_anims.bin', 'details.bin',
                            'stores.bin', 'invstoredsalvage.bin', 'tricks.bin', 'visionphases.bin', 'invbasedetail.bin',
                            'powercustomizationcost.bin', 'invsalvage.bin', 'baseupkeep.bin', 'attrib_descriptions.bin',
                            'version.ini', 'items.bin', 'replacepowernames.bin', 'experience.bin',
                            'loadingtipmessages-en.bin', 'powercustomizationmenu.bin', 'attrib_names.bin',
                            'villaindef.bin', 'pc_def_entities.bin', 'invconcept.bin', 'pc_def_ui.bin', 'salvage.bin',
                            'kbkorea.bin', 'lods.bin', 'villain_origins.bin', 'exemplar_handicaps.bin',
                            'pc_def_unlockable_content.bin', 'baserecipes.bin', 'tailorcost.bin', 'villain_classes.bin',
                            'behaviors.bin', 'customcritterrewardmods.bin', 'pc_def_destructobject.bin',
                            'clientmessages-en.bin', 'seqstatebits.bin', 'pc_def_mapunique.bin', 'clothcolinfo.bin',
                            'powercats.bin', 'supergroup_badges.bin', 'powersets.bin', 'boostsets.bin', 'costume.bin',
                            'product_catalog.bin', 'data.ver', 'villaingroups.bin', 'combine_booster_chances.bin',
                            'npcs_client.bin', 'animlists.bin', 'defnames.bin', 'mapstats.bin', 'roomcategories.bin',
                            'schedules.bin', 'detailcats.bin', 'supergroupcolors.bin', 'soundinfo.bin', 'ent_types.bin',
                            'invrecipe.bin', 'boost_effect_above.bin', 'proficiencies.bin', 'clothwindinfo.bin',
                            'capes.bin', 'kb.bin', 'map.bin', 'pc_def_mapsets.bin', 'behavioralias.bin',
                            'boost_effect_boosters.bin', 'loyaltyreward.bin', 'cards.bin',
                            'combine_same_set_chances.bin', 'classes.bin', 'pc_def_contacts.bin', 'mapspecs.bin',
                            'auctionconfig.bin', 'menuanimations.bin', 'pc_def_nonselectable_entities.bin',
                            'client_settings.bin', 'pc_def_animation.bin', 'badges.bin', 'chestgeolink.bin',
                            'conversionsets.bin', 'plots.bin', 'visionphasesexclusive.bin', 'roomtemplates.bin',
                            'costumeweaponstances.bin', 'supergroupemblems.bin', 'command.bin', 'defaultbodycfg.bin',
                            'origins.bin', 'combine_chances.bin', 'texwords.bin', 'dim_returns.bin'}


class CohPiggsExtractorTests(unittest.TestCase):
    def test_functional(self):
        test_dir = os.path.dirname(os.path.realpath(__file__))
        test_file = os.path.join(test_dir, 'data', 'bin.pigg')

        temp_out_dir = tempfile.TemporaryDirectory()

        strategy = src.coh_piggs_extractor.coh_piggs_extractor.SimpleFileOutputEntryProcessingStrategy(
            out_dir=temp_out_dir.name)

        pigg_file = src.coh_piggs_extractor.coh_piggs_extractor.PiggFile(test_file, strategy)
        pigg_file.extract_files()

        actual_extracted_filenames = set()

        for path, subdirs, files in os.walk(temp_out_dir.name):
            for name in files:
                actual_extracted_filenames.add(name)

        self.assertEqual(expected_extracted_files, actual_extracted_filenames)

        temp_out_dir.cleanup()


if __name__ == '__main__':
    unittest.main()

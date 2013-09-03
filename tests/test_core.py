from maflib.core import *
import unittest

class TestParameter(unittest.TestCase):
    def test_empty_parameter_does_not_conflict(self):
        p = Parameter()
        q = Parameter()
        self.assertFalse(p.conflict_with(q))

    def test_empty_parameter_to_str(self):
        p = Parameter()
        p_str = p.to_str_valued_dict()
        self.assertDictEqual({}, p_str)

    def test_conflicted_parameters(self):
        p = Parameter(a=1, b=2, c=3)
        q = Parameter(a=2, b=2, d=4)
        self.assertTrue(p.conflict_with(q))

    def test_not_conflicted_parameters(self):
        p = Parameter(a=1, b=2, c=3)
        q = Parameter(a=1, b=2, d=4)
        self.assertFalse(p.conflict_with(q))

    def test_dict_with_parameter_keys(self):
        d = {}
        d[Parameter(a=1)] = 1
        d[Parameter(a=1, b=2)] = 2
        d[Parameter(a=2)] = 3

        self.assertEqual(1, d[Parameter(a=1)])
        self.assertEqual(2, d[Parameter(a=1, b=2)])
        self.assertEqual(3, d[Parameter(a=2)])

    def test_dict_with_parameter_keys_modified(self):
        d = {}
        d[Parameter(a=1, b=2)] = 1

        p = Parameter()
        p['a'] = 1
        p['c'] = 3
        p['b'] = 2
        del p['c']

        self.assertEqual(1, d[p])

    def test_dict_with_parameter_keys_not_exist(self):
        d = {}
        d[Parameter(a=1)] = 1
        d[Parameter(a=1, b=2)] = 2

        self.assertFalse(Parameter(a=2) in d)
        self.assertFalse(Parameter(a=1, b=2, c=3) in d)


class TestCallObject(unittest.TestCase):
    def test_listize_source(self):
        self._test_listize('source')

    def test_listize_target(self):
        self._test_listize('target')

    def test_listize_features(self):
        self._test_listize('features')

    def test_listize_for_each(self):
        self._test_listize('for_each')

    def test_listize_aggregate_by(self):
        self._test_listize('aggregate_by')

    def test_default_parameters(self):
        co = CallObject()
        self.assertListEqual([Parameter()], co.parameters)

    def test_features_experiment(self):
        co = CallObject()
        self.assertIn('experiment', co.features)

    def test_equality(self):
        co1 = CallObject(source='a b c', target='d e', features='x', for_each='p q')
        co2 = CallObject(source='a b c', target='d e', features='x', for_each='p q')
        self.assertEqual(co1, co2)

    def _test_listize(self, key):
        queries = [('a ab c', ['a', 'ab', 'c'])]
        for query in queries:
            co = CallObject(**{ key: query[0] })
            self.assertTrue(isinstance(getattr(co, key), list))
            for q in query[1]:
                self.assertIn(q, getattr(co, key))


class TestExperimentGraph(unittest.TestCase):
    def test_empty_graph(self):
        g = ExperimentGraph()
        cos = g.get_sorted_call_objects()
        self.assertEqual([], cos)

    def test_path_graph(self):
        self._test_graph(
            [('c', 'd'), ('a', 'b'), ('d', 'e'), ('b', 'c')],
            [(1, 3), (3, 0), (0, 2)])

    def test_tree_graph(self):
        self._test_graph(
            [('b', 'c'), ('a', 'b'), ('b', 'd')], [(1, 0), (1, 2)])

    def test_tree_graph_2(self):
        self._test_graph(
            [('b', 'c'), ('a', 'd'), ('a', 'b')], [(2, 0)])

    def test_tree_graph_3(self):
        self._test_graph(
            [('b', 'c'), ('d', 'h'), ('c', 'f'), ('a', 'b'), ('b', 'e'),
             ('d', 'g'), ('b', 'd')],
            [(3, 0), (0, 2), (3, 4), (3, 6), (6, 1), (6, 5)])

    def test_reverse_tree_graph(self):
        self._test_graph(
            [('a', 'c'), ('c', 'd'), ('b', 'c')], [(0, 1), (2, 1)])

    def test_reverse_tree_graph_2(self):
        self._test_graph(
            [('b', 'd'), ('c', 'd'), ('a', 'b')], [(2, 0)])

    def test_reverse_tree_graph_3(self):
        self._test_graph(
            [('a', 'd'), ('b', 'd'), ('d', 'f'), ('e', 'f'), ('c', 'd')],
            [(0, 2), (1, 2), (4, 2)])

    def test_diamond_graph(self):
        self._test_graph(
            [('a', 'b'), ('c', 'd'), ('b', 'd'), ('a', 'c')],
            [(0, 2), (3, 1)])

    def test_acyclic_graph(self):
        self._test_graph(
            [('b', 'f'), ('d', 'f'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('c', 'f')],
            [(2, 5), (3, 1)])

    def test_hyper_reverse_tree_graph(self):
        self._test_graph(
            [('d', 'e'), ('a b', 'd'), ('c', 'd')], [(1, 0), (2, 0)])

    def test_hyper_tree_graph(self):
        self._test_graph(
            [('b', 'c d'), ('a', 'b'), ('b', 'e')], [(1, 0), (1, 2)])

    def test_hyper_acyclic_graph(self):
        self._test_graph(
            [('d', 'e f'), ('c', 'd'), ('a b', 'd'), ('d', 'g')],
            [(2, 0), (2, 3), (1, 0), (1, 3)])

    def test_cycle(self):
        with self.assertRaises(CyclicDependencyException):
            self._test_graph([('a', 'b'), ('c', 'a'), ('b', 'c')], [])

    def test_cyclic_graph(self):
        with self.assertRaises(CyclicDependencyException):
            self._test_graph(
                [('c', 'd'), ('a', 'c'), ('b', 'c'), ('c', 'e'), ('d', 'b'),
                 ('b', 'e')],
                [])

    def _test_graph(self, edges, order):
        cos = [CallObject(source=src, target=tgt) for src, tgt in edges]
        g = ExperimentGraph()
        for co in cos:
            g.add_call_object(co)

        sorted_cos = g.get_sorted_call_objects()
        for former, latter in order:
            former_at = None
            latter_at = None
            for i, co in enumerate(sorted_cos):
                if co == cos[former]:
                    former_at = i
                elif co == cos[latter]:
                    latter_at = i

            self.assertLess(former_at, latter_at)
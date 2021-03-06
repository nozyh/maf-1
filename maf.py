#!/usr/bin/env python
# coding: ISO8859-1
#
# Copyright (c) 2013, Preferred Infrastructure, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
maf - a waf extension for automation of parameterized computational experiments
"""

# NOTE: coding ISO8859-1 is necessary for attaching maflib at the end of this
# file.

import os
import os.path
import shutil
import subprocess
import sys
import tarfile
import waflib.Context
import waflib.Logs

TEMPORARY_FILE_NAME = 'maflib.tar.bz2'
NEW_LINE = '#XXX'.encode()
CARRIAGE_RETURN = '#YYY'.encode()
ARCHIVE_BEGIN = '#==>\n'.encode()
ARCHIVE_END = '#<==\n'.encode()

class _Cleaner:
    def __init__(self, directory):
        self._cwd = os.getcwd()
        self._directory = directory

    def __enter__(self):
        self.clean()

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self._cwd)
        if exc_type:
            self.clean()
        return False

    def clean(self):
        try:
            path = os.path.join(self._directory, 'maflib')
            shutil.rmtree(path)
        except OSError:
            pass

def _read_archive(filename):
    if filename.endswith('.pyc'):
        filename = filename[:-1]

    with open(filename, 'rb') as f:
        while True:
            line = f.readline()
            if not line:
                raise Exception('archive not found')
            if line == ARCHIVE_BEGIN:
                content = f.readline()
                if not content or f.readline() != ARCHIVE_END:
                    raise Exception('corrupt archive')
                break

    return content[1:-1].replace(NEW_LINE, '\n'.encode()).replace(
        CARRIAGE_RETURN, '\r'.encode())

def unpack_maflib(directory):
    with _Cleaner(directory) as c:
        content = _read_archive(__file__)

        os.makedirs(os.path.join(directory, 'maflib'))
        os.chdir(directory)

        with open(TEMPORARY_FILE_NAME, 'wb') as f:
            f.write(content)

        with tarfile.open(TEMPORARY_FILE_NAME) as t:
            t.extractall()

        os.remove(TEMPORARY_FILE_NAME)

        maflib_path = os.path.abspath(os.getcwd())
        # sys.path[:0] = [maflib_path]
        return maflib_path

def test_maflib(directory):
    try:
        os.stat(os.path.join(directory, 'maflib'))
        return os.path.abspath(directory)
    except OSError:
        return None

def find_maflib():
    path = waflib.Context.waf_dir
    if not test_maflib(path):
        unpack_maflib(path)
    return path

find_maflib()

def configure(conf):
    try:
        conf.env.MAFLIB_PATH = find_maflib()
        conf.msg('Unpacking maflib', 'yes')
        conf.load('maflib.core')
    except:
        conf.msg('Unpacking maflib', 'no')
        waflib.Logs.error(sys.exc_info()[1])

def options(opt):
    try:
        find_maflib()
        opt.load('maflib.core')
    except:
        opt.msg('Unpacking maflib', 'no')
        waflib.Logs.error(sys.exc_info()[1])
#==>
#BZh91AY&SY��^ Y�����]H������������   @  �`U�z{��uӚ6�����y�5{eP�R�ک^�ҩP����{^n�^��O�B�l�7��s�'��   to��{�}�����w��om���������{٪� )7^�nw���w�y�>'-�u������o��}q}��ݶ닷Z�xuU������(z�j�{]�N�O6�[�sO�|����o�]�z�Ez�l��i�Ǿ��{�k[7w=��h@D�O�)���@�F@� I��4Jh�a��dԏ#YYYF�A���     �D@�M�����@��2�i� h  #YYY #XXXD�FF����~�6J4�S�iCd�S��F@  �$Dd&ɕ?Mb�<4��Hz��<�i4#YYY���A2��4�S�Oj����=S�g�=F��z�=@��#YYY0��o����=�9��(�U7Pо�^��ޜP��>���a%�9-�h�{��$�#XXXYZ�HL	������TI<��\M}��n~��4~�W�m�0����i>_u������͟*��[�Q��3y��U�z�蚅�BB1�ʒ��;^:�a��A��gd¨����O^�q����O�vkM�&�Djd�ީ����z�����]�1��>2�M/cZg�h1	̉�w#�ζ��2�(�pDD�O5�.|�۳�V���M ��g~�6?�-� �	 �	%Z�8�j?�E�m��X�5m0t����?�_�R��_�a��X� ��.�Y����{�c�<��H�s�C�:Co�������=h�ЏM�P����!F�:�u�B��߇�5jB潙B1@83N� ��y�>X��roB�m��+�(&#XXXG�>�Z~����Wv�4z��9���a�熹|YΈ��ɹ�	0����n���99����X�Ҡ��3�#'��[����ְ�d���� �%��he&>Ըtt�:e��y��ы�~λ�t�D��������l�3*������������ӱ��Z��U��! ���e=w���bvY�1n#�(�r��O"Rtg,�#�W��CK��{c�v�כ=�-.#��UG�9���]5�y�Q%Q6�I�bmo�l�����S;���[���؁��:�iL�+P<�Y����[a�%-Y�Y�x�+;)��������8�����h1G���[�����~/��7�c�f�a��c�S�����K��ل�����ޙ��|H+�ASz�A2E�0����	i6��Nސ��w���>G�Rs��^ˇ�$��I�̽�Ǽ ����L��@�	O���b������U�����#XXX��w���O?��ې�^\<m+S�@��RdS�>#YYY����7���Ù�׎KRG��8g��CN��R�MO_c#��.z�njթ����إ�ݴ1\�^}I��������I3�ddQ(E�-tY29i�J�f���R�G����vu\s��G�/����d*��V�ؘ��'m��h�!#�P�S��6.�������ð��WO�m�����²�����a�#YYY�cO7�"��������}�Q�������[�}܎��Ӄտc����#YYY>}�y�\�������y�����`(.<���]a�}*%ǐ�:���K2u��A�����47CA�mI������p��^�[E4v�n, ��)(�yo{��XH叟	��y�֩4�t݉tr<ǁO1�����x�cCS@���s�}!�C!�AY��'��̓���c`� H{�L�z�B����ML��y{:]U��n�h韴�C��^�p%%Y4���ѳߍ_,&������C�k�J��w���U7�M�V��g�[X9>�mCm�+e����_���v�\�M���O�r]��p�cXx]�8�D5�"7wM71�U^�a0�C`ƈa�2*ͅN��m��h�Vi�L"�,V6��2�n�$M�U#^���q���q��~Ri0����}���Y	� V��`8!o%Ӈa�	�Z0u�o ���ۦI�� fiMc�6<�!x�Gѧn�ۨ���O�|d��y��Gd�C�Y�a��'�M��_����q��Gw�n�u���*W��9wcGb.����]A)z�#XXX�7h�J��0[a���#P�ݽH0����#�1h���m�����z�L:���Ӧ>�9�'�#YYY��%d^}��: B�y�y���#XXXs�����v��pG/�w ap$�\��fv6�f�!u��A7�c�׬@�"j�H77�����7�M9��LK� �q��x�'9R�!.��V�VLf4x�e	Ěou.v��9@v� T}���k���J���=Ԙ�ʫ���I#XXX��r!4��hWb����F_|I��Kx�-�7Ie��T��%�#�]l��}"���7��a�Z�%�G�i5Շ��B��$W-�Y_`�N6&{��}�d�Yw� ���Lq����:0�9e �>ﴤQAV0��"���k�~�,%�2a#XXX�~���Ԅ��\?8�Y'<����#�V5R:�x�u��B��s����X߫��zy����o�l癹�3_C�x�΋�e�[�R�58Sݰ���H����;7��'K9l�B�F����6M�c7�1��ηٜ6��9	2GlgAz��y�m�CQ��4uъՍ���hK�|�B�O�PxPK���Q����u)P-/԰�JQ��6��(��=��ț4-z6L�mW�S$�h$�d�8���#XXX��rʏ�O/>�H���X���ݪrq�����x���+t��w`ӳ���R��Q:w�џ��7�$��PCi.G����Z*������Ef�.�#YYY6.�.:�T�[��)�3eP[@�R2�P�} ���{rf��Y7�wH˶)y�nѯOY�@z�Us���g� ӓ�+�3�kG�NVۑ��x��`v}?�sXڸn���l`J�#YYYX����#YYY8Ej�ʧxs��4S���^5d����Z��('��r��z���0����1���g/mVxv�Q�#YYY?X�V��vB)��/6%1�@&��l��Y4�ȅ��S�jYv�t�by���J&�k��p���j�ϒ�-;���q�M��o$����Mq�0��P��S�Ǣ�M{�R!��&P��f����>z�Y�I��˓��2��TZsc��0X�Gv�l�U.@��pv�#�s=�d5-��U�G���7NC!�����\��w��� �1�#XXX;kN`:����8�[�-�+���;#XXX��e=^��Me�;9 �(���e�� �s.��wX��X,��6wpʁ�=��˾�l^t�����M��&̲K����[�I4�E��|y=�/M�vm&���Cʋ��m/��9`�7gpl{!�5���,��ğ!)��β�n���%�A]p�f��o<�ѣ��s�Нƣ��2f�:ϫ:w��\/��y0i�q�;H��@�n��`��2�?�GlUcƗh#XXX���)�B�Aͩ�ܷ�7h�*r�k���f �J	���u��tī��.� � �J���H�g�H	�����21iLZ-.�,�`�U9]��GE삭a}T�<�L�VL��V`�kX�oF���1A8��-=|�_��X�+<���M �K	)ct�B�-�'1��B���G��kD�;�VĄZg�qn�el���f+����x�[JP�n�'M�4�t(�F{�i�UW��[�����9�魨�w�̕�|#YYY��^_��s��F�oTl���6�`SDs{�y�1_�h�jv�H���|����Α�a�mf"K�v��PBi�#YYY�����K##G^����P�^�$�d�sI��P��s����,�	[D�4�Ԇ�69 �� ��;�Ĵ�iN&�s�-�4 g�^�	��<�t�X�,%�OH����� (3T�ŨH&c#�ͷ#YYY��K=��p"��ׅx4W�蘜�Dm��#YYY�'�)����ȶ�\�`��D������oɷ0���η�frf� �'#XXX'��ym�͓U� vҠ�L�i�;6<�,�F��M6Y����ك�9X�+��}�<���t��9t��� ⦟��_�F�j�Hj���JM'�Jc$1D�>�N~���8�#�q��[����R���r�T�o�Lp4�:z���Bm�}U;�{,��O���ax�~$C�. 8#YYYa���tIA>6����7��&����Nhq�G���wG��z�o��?P��{�_o���E���<�8�tZ�&a�_vV����z����P�Js���u�6� #XXX��O5�p��%�xA�q;9iuq�FK��ڵ��D�h1��\Jp<�{su�DD���û!j֊ʫk��b��b��G����zi�_���QhDo�#XXXh�P�D�C�;���	9[��Ws#;��mrt��^o���S�훏�%Ц�iu��1u	@�_�4<<����X�S�Ӿ�Q����`���Q���l���ؑL�S۷��$�V�*�c��<Xr���rծ"�r$�S�&�i�����I�L&�ܧO��I����3��������ɥ�㳍N��k[8�l�<Y���j7se�'g*�w5���Պ��A�u�Y�����S��Ħ�4�&�!M%����T3�6�GL��Z�vds!��ߟ���*��m� ��Xm62T�o!�%[�8a)�o�~(/z͏���d�%j���oIym:�:�!�058<w���%�e��/��{�󜠡o~�1��(��ƍ�jLH�ҹ��F1��B���1kQ��k	:�<�����FV�;!��#YYYg��z��˦Q���?(��Bȳ�������t���F_^~	9q�$d��tg�F�.�q�����8,z�����)i!q��ҙ�z����O^���e�|H���nK8!�l�j#���e/5e�W�p��;���������q��+�Y�#YYY�F�N2#YYYF~Ҽ#YYY���� ۊ�/t#���2��vX ���LF�c��:�?���r����/▇7S�7��P�`r_W�a>[&��#XXX�� ����<ݝ�'���s����{�GP�Uo�dyB�#XXX����w�uUU[V�k��:~@� �F~���O�S���G��~s���r7�{�x�{7gӄbC��+R(,����|���[ʢvc�s���3[T��B33�������K=a���ۚ���{������R��6�l�?)¬.¢���@}�j6�3�u"ݨ��b�� �3p�$/�<:�����7-)K#3�KϛC#XXX��+�Z�(L�������nS}sL��9���C�j _p'W"����{�{��?W��_#XXX�N�xI�i��e�6��:qkU�����&g��AS��gϧ���}W�l�mx,mJ������;�x��^�$��S����#XXX��#YYY��Ä�?/	���m t�8��#XXXc�����Vz�;�=�v�S&m�]T��>w;�GL?���j{m��m�̓�8��	5{����[��E;��pF^q��˲c����[p17�j�O�<�T}=�= ���˝^��u���ka�i+&.3+3�#XXX����ca��*�^�aM�]"�ޡ�Xo��@�#YYY�#YYY�t�����^��#=kB��FY��! ��qw����m�I��<6�y���տiA5�	1�24��J�L� �!́?'{�|{���>����d��0�-�R���#YYY�M��]n��T�ix�s�BCK�1�ݘuk^(�tfk4x�S-�O��^]f5�5�;#YYYs���?���<��Xw{��w�*����oH������)�K7hO���eo5.������⟆Ӊ]��Ѓ\yMaA���Z1�M���.��dm:�[��.~�t��^���#YYY�#YYY8���d#XXX�\�׼�>wO�>�=�G����f�6����A=�������d"�#YYYF��\���A^��D�%����o��C��_o��R��g-��4D	O~'���	0	~�%1��1_�g[cmR����ȭ�!�D4��W�zt�OC}o{�$�����$L�Ǖ#XXX�"g�8��$5@aێM�z2p:G��3�ۘ}i9�;u_DC@ؔm��z�������g���W��[g��쎢I:Ҟ��;	%"�u,4:(X8����-,o�q��/�u��ӆ��lP�0uy�8u�;z���?�p��:�:#YYY����da�ADC�2r#XXX�ʏ�&��0L�A3PUa��;|����?��jL����� �#YYYJ���͘�{P�إ��Ţ#XXX�3r�uMT��	����q:sۨ����dـJ�j6�U�?�O���#����l7�?�R����Mƽ/ˏ�o1�z���G�Mo��-���'���(�+��O�52v�y��)6cA���î���>I<zB��>�J��`�J�9���`��u�SA�'Dg����z�)<�#�`��?9�������v�a�l~��ML������������:Nc���=�������ץ���ߛ5l���|�����a�[�c��B�g�*h�#XXXn�dd\����wj���sʇ��R������a��I�)���R{^>���g�>���545�24�(�>�w�p20}"�:�g#�>���k�N�m�i�;���e�Y'i��������p��dx���`�J��>�����o00Q��5����SqL3c�4�SP�ا��y&ۍ�qM�`d�5�Y:m}u��,��[����1̩�Pr���h�ĝG�z�&�E$�N���醣����b��Y�&�'�)=�;��*��~0����X�~�3�?��g����=�<�`�Ԟ��y���Q���&#YYY�(���ɓ���$囆:���ω��Q����u�GY���`�����hhdd��7��Y�-��ˇS�L�;/a��t���ОC#C^����f�N%q�N����{�#YYY'��1f<���~���Iv-��T�	5S�����Y��7�z��S������n=g��{�#YYYg��'c�:w�ݴ��ة�jz��GA���o�5��|֪>�������c&�s���H����<5��/�hM�>�T#XXXn�&`��I[>ߺ#YYY���I���p��SL��瘚9�:(Y�O��w�t�jh�E��m��x	������{G�;~���Ze��br}�o�79�������v>��u�~�o���a����Pl9ʡm����ĉURvq�o��^�bxz�D%�7e�k��<Tі{���Y�[�i�̓�y DErHr��y����wghB��ܿ�<d}1�����2���!����q�&A��d� ����c�/u�[�>#XXX:R��'s���B4*6t#YYY��A�kqP�;b\#YYYY��Rue�oު�a�l8�,��b���{nXCѺXl6r��4K��&�KA[�ݽ��j�9�5�������W�k�LR���'�����&0�}��/����@�ɗ�w�GhU���H=�v67�9%$�5���g\#XXXNGp_"rJb%��k�g��y�����M8�oK�[/���n���������.��T&C�^���X/�����<�k��w�x�r!)B� �E��Krd:��=��h���[w��I�S4�gG#XXX%��Lv�ơr��P���(uz��(+��N�1�P������e��[jZx�O0PZ�gN�aϟ;`m��Q�be�!X��6�#YYYF�h0��>?f��Dd��P� $�����͚�f\�Q�Щ6N�7M�g����OX�O�м�0�9g2'�"�*v�% 툞Ny�#XXX���#XXXj����:���U0'ʑ�$V#XXX����W����.����dZcǇ��rf���\�U����vlԼ3�_��4����kG����N�;����ŀ0$T���ԇ7��?T�2$��H��O$5��D�G0JP�6 ���3L��F!��^�$�N=r� ��#��Lgb+��ݭ�rw&K�>�Hx�"n�:W��T:�$�R���B�"�#�:v�3F�3�@�ޕUP8����dtmBI"��t��P���c�:%D�T��ӡ�[���;��a])�ت�򅲪�bB�	e�I#XXX�7UlD����<�cwu�#XXX����Ǥ#YYY��ة�%�����^Ȧ<}��g΂�C����a�zB̕�@��Ŭo�P` ،�Z��}~��8S��\;���8e�< �L��	�.k�;}���UXy����rC���f�iG����~���l1I�TN��C&|QU�9`j��!H��^�K��8qK�E��$�O.v�04;zQ?#XXX�V�`�8�H�W��J���t�$�)�Fq#��,31���#st��&S���W�[wI玮�W��4ٻ�\;�;q�&G�L	�l�"^p�<%��~ĝ��6�%�(툺b�1��̄`�����3�y-)���2I$���Xf5B�9����5̿��^ �S��\�Dt'"�R�U4�����h�ײ5�wI#XXXsM��?�>�q�@jB?"�9�繵s���ρ��哊����6tg-V�#XXXiN�<�p��:�N	�����aOH@u�� ���g6m0��pa��K�<��U�s�2~yr#XXX�(4F�s�rUo���1q���)��5����b�&�mL$#YYYHJ�K��MH�,�uZ&�14�@ƿX�NlWK5�Qi��%sN�eMFG����Gէ2R�����+�Y�\IN�źj2F2��#YYY�FF.�2���Im�m� �"G�ر�%����78�z������4?�H��A,l�g}j���#YYY)�@�A��Э�C��"h�8�M.��Ԓ@���+J�����2h2%)��;[$i��WN�֙��1�R�����c���r�z�:��8rQ{8�uKeT{�UC"�h*��2f�pȋ*1�p"�Z�`G>=�r�;���s�}7����d7o"�ᣬ��я*�b��2��q����5�XYg�����<qCtv+[P�w�t�5��ap,i���/M�f���	j���S��	��ż�-�`Ӄ$,+��,�:Q��7@@(���������?n?Jfͽ����%n�SD�^�v�Y����j#YYY��&�g�V흧�����E���Sm&k�\#YYY98F���-���:�:�6Q?�<Vi��9���Њ#XXX*�9�v�I�湲:�b��w5����H#P�s�͔��\BO,����U-&�I�=pꃪ2&f��jtk+#XXX�6�s�xM��ı��#lv���<ް��u�ŭǡy�v�g2�lð�$v��<7�P`�,�Yc\�I�vuS,��`��r�W��ư6W��7q����7;,��\�a� �|�'#YYY�#�G<5��q#YYYm;��@&Ljp���cO�kH�#XXX�ӱ5g!�[�lqpg|i5��i%��<n��b[+�=8��\#YYY4Q��gӏ<b[���B����	� =O/�|o�r��+�0��̮�X�V��4��2���-.�j��n^k�n�C�M����`�M�]�q��;�����LL�s����j��NN�]`Q9��Czm�s�|)ނc$黷�=��wc�GvF:�5|#XXXv!��P�B��a�1���6��x��;9�$�k#YYY[æ�v�`��Ga7�ljsH!b�:B`_+���wR�5��6罈���,?5��h!�vp�.�|�_�>}�(5��0�rE��0ξ�S���`�HU~����G��Q���$p�d�>�f1	[&S0f`˱+���c���gC����8^M��;9f�6ɥ��`M|/���3V������<�am�j��F��pm���P���.8\��<h��d�Gf8H����aʔ�Cwg��2�z���\�x��f��8�`���ť���^��1^j��GO�@��o(xFU��廆��ovT��Bb���M���<�>���$)#��g��h"8���_����|�< ��"��L���0l�����#XXXԍ�F2�3��#XXX�S$c��/m~�ť�ۖ�ݿ�e�YRz�;�n����#YYY���PK�=��I��&'#YYYC|$�|i��v�sI�(�3rd��"2L�f�m�#YYY����xg$K@�S)"%`�������|���B�ưT����yq�tWUJ�6�z�,�b����3��6i��9Q�"��W�bG@Qc)��R3)���'D�d��L��UK0�EI�ٷ���`�T�n��[�Qi3K�i�]$[�xyÌ�ܙ^y�F�a�錔�*�ŇVL1�ؖ�A���8l�L#�ɁU�i;l���i�l���~n���q��0 �Վ��f	�Xv�&4@0C���^#����` �+�~Rj�\v�#>B�X��GB� ]=P>^�-ZW��=Xگn�a/�Hẑ��P/�#YYY���e�~Ё�Q�D����~�w�T�&'晓�-�bC>c :H�H=¦�Ě�T`��1I	#�jr`B5e���hq5P�l����n��[�#XXX��-�?f����6"�.0�)Yd'ϻ0�4��mP��q�R�OI+`�+i��y�BEu�~Ga�H�ߞ	d��z+�*���l�^����Qya�9�O�7��tad�A����]][�/�ez��)�S��,��ȍ`�9���L�!�2�����41#��*{��Ny�^�������ܬ��`9YT��W7\r�Ny0�j��sD}M��+#XXX7v�g]7�S"�^�ŶY�N�8#YYY{Ҭ�q0��a�������?�����+V�4�]�1��ՈC�����9��<߸�L}��2�o&mɌFX	BE��\�Ɂ�MLY#XXXd�%�u%-��l���w��	�LF�#̀2ii����@���i)J!����[��cE]І<��ȭ�G��'3��ME%P]��P�)����#YYY(q"�Й��+��>oU^�07! �糫�I#YYY!��e�uN���o���g�k?���?6�b��0�'g�ߖͮQ�R`��%'��%�ȽhN11!�g���{���c�U"%JP�o��b�8��(�V@�24jF�9��T�e�1��%�R�<eG���=��G���GBl�{����ئ�iy��xbW%l#YYYH@v��wLT�t����̮�Oi�#YYY��iZ��a.�F�$��s��ʦ��0v�y�,9�N�T�zl�S�X��T��<V"UP����0�z �@V��X��KB��C/��g�j����zIB�e��E�øMG��?�|�_QdYc`<����=���o#ɇ���ʜ,�#��E*�e�0CE4,4�!!2�����)�OE~�#YYY�g�E;�}�{~�^����w�Ή�"�}��A�$RT�f`?+�uPQI��(��>,�}}��`؇���S���4D��? �b�&%ⱻ��\;�`�w�+_���,�n:�v:�#YYY��}9�Am�#ڐc�o�q#�,m�P��B_��� ���z!�$1d��0a��T�D���'�2&�9�D���a����r##iJ���}9s��@���WkDf8!]�2H���Cn>T�h�L�mo�������=�F�Zc����ǰ���6�Ǭ����:0!�r��x#zɝ�SW++� 0gբ*0h���H�*QL46��l���k���� �IA�������B�sU)��8�t���#YYY%��ߧ������ן�G��Һ�tC�;�l'�(�R����k#2oSHx�&iLm�T���#YYY}�_3x3k���D	y���e�FXHȘӏ)%$F�#XXXH_HN�Rҍ��pYwނX��+�1������A��lC���Ws|9=6e���޵RQv<�:#� >޿��B��a�!��!�Y9T҆�N#YYY��颋0Ӯ��&+�ɄO+v��ј��Rx��vvY���-��*{��O�-TL�i�	��m�L�.)͸�"�m�q�k!��6n��̦���c�V��p��EE0#YYY��p}5�-e�zt#XXX��p(��*	"L�vh �b�L0#XXX!��a���1�t�Y�6��0#^�ڑyȜ�4H�H|�������}�����Ȝl:,��,��ɖ]j���LχwV~]�3'���a=!�O#YYY�#'l�q)�SpPt�`���o ��aL�lev��hL*�07���"�	�s%���.lA)�L�z��%���ɯgY�N�)�����|��/PH���ץNH]�L�5A��'|� ;"��V�H��x�s'+d���l#XXXe��MT�=q#YYY*M��d!�;c���o[�I�<�4�`fDS#XXXِ��!f[��������#XXX�^:_����t#YYYP@�F���1�<�10 �F�]�n�uݻ[�*"��	r.,��E�ָ�����HZ5Fad�C�.?9<C�ZrS�Ig�=���	��}٦��jG�1I������ƆX��(ɽ��S>v�@�x��ŗ�{�Z���pU�3��qr��\��,�,I.�L�b)�Pe �1 ������ӉF;�4.�a#YYY�0��b!��)�hi�� ��x�]���lQ���l�eW#YYYJ�i�R������8�X��u�iA�`ySx�]Ox<�*4&m�ͱ�B1o�=ka$䑌HT#Ȇ�t�/)q����0yɻ	W~���!���ܘ�5�/#YYY4�����iuX�bl�!V6&f	�#b�`���h^~��Ov�N�P{�+���e`aإ�`o���!��墙����-�.�Q��N$������sq�s4�@�A���ɀ�;��F@�I�8 z������{���#������C@i�(��������	₢f��|�:���a��p@�D=��^bs�41'`�40������?y�,r��$�c�CR��Lp`��514'L0���B	=d"���HRY��iߏ�8�UMO��=�ۇ��#XXX��*��=��iw�y���۸�w2P@�9�𵂪��&�х#�)0�Q�����p6��)55�M���#YYY f�!�p),m�C�h�X�h�u�� ���(�+!�:z(���[�Jo����%PQ�'�v�� ��O���M���qT��0�4����:�Vy�T5~�$�֟FM{���wI��t����X�����R|�O��˷Xt~��O������C%��6�l�fU�p��~)�G+�a��ȩ� �-<�1�@�T��\_��,1i��/�0�j�1�鴘�b#YYY��c��O�#YYY��G/���TIEܓ>z�5�|X���im���is>���:i#YYYI�Q�<�>0o�f���u�0i.i��9����Uffeq����k��m>����B��-'���[�cd/δ>b9C$L3Gt@$R\���Cp�<[a]��<��P�>�=֝8#XXX{�3��0��A���`&#YYY�y�c���K�C�h���򉠢�#Q�I��Q�;y��1��M��pp��B�lp�33�dU��I����¢�7"a,JNBd�d�2�A!<A��Xf��F�$&�#3�+�A��(���Z%0��!�d�IQ1�9�`��M���.,I0F!�;��| pũK֩��S��n���,��N�q��6/_��M��o�#YYY��7)�p�ލ#YYY:��Xc��!�l��Ep[��r����H	�1�L��!���&*�n�����v�R���x�#��C 冩�0�gp#YYY�9\�|�:W+�&�y�_�p]����U:�_}�|τr0��r("�0�P�TZ���љ���k ݺ�=^��A��܊Z�I|!}���#���h&��mGv0�lv���I�+V��(�*���ràhL3_z�î��4���l�Z�&�6��D��`܄�h��#$0�@�HI,�jIn�#YYY��c��!��k/T{���I%\;%J�h�z�V��i�#YYY��J�#�JzQ�o������|���3"����ʞ�uS���������s�0�!>�zU��)$���-r��sXִs4�ᴚ%�Λ�5�c��k)fL�\�+'-��IRT�� Y9q�3V'w2�6��R���t:Xr�\i�SUJ��u���)C�e=�ѐ;d�}yM�݅x�rRZ�V��CN7!X`�e�xs�� V����O�q#YYY��M�w(MI��<L )0�JWk&���h�C��g�Ҙ�1hׂa�ݑzDcq��ȌEyjmX�uд�o�BHd�}ۣcO�q�on%Z����e}�ۉ�e~-m��ĵ<l�p�î&MvXd��E.%-&[08��P��ĺyL[��H<�QL��z@���v��d���W��Z`5�(F���ιS����`C�>4S���f'��IՀ��c��lkM)T�՝���-�r���fyC�"���Xf3+2�p��=P�eT�tnHb:���Fvۯ��ܦܹ������k�K��g�x�"�NBw��V[7��w�b��#YYY8<x�ٜa���|	'd0 Q�FF߶�J:8|����ܒ��kF/Ԙa��g����Æ�cq��J��ӝf̐tr�lm&57-#�B�����եx���&��q�r�y�*��H�B'�PQk���)�lD�C����i5�͖��c_F`͆M�ah���f����:��!#�k����p�~�B$( )Ie��X����yl&�-�,�ks�L{���0R�fd#YYY�7���ӧ9���KHM�,h��	#XXX!�+��=���t�����͙�S��6����!�bt� ��(�^�r�[���z\�>7i/J��S)����PC�y,юs�ۙe[e�UYF�n�#YYY9`�[&��$�l�Ĩ�{c�s�l�u�$����z@�ۤW�>�>X��(#��6	�v�l��7��f)�G�x�#��rs(\���F���΃e�����k{+,�d�]�&����胺ݕP:9#1P�N�q(�|��iL��8_�!���F3�7��P��^��e��l�T�jS�F���hߗ�����9����J�����X���üI��5�#XXXA���y�*�t���EV�h@���z�#XXX�8����UR�]YTc�mi$�ݸp=��8�!�3 �����m��rd�Hj�ђBQ{���3���xt�uß���J<�!�$�^xu���\�k�Ps��Y��9zY����m��;�m�¯{�WQ#����N�YMX�r1�x�;�QC�5��B(���oy(H�7!�32d�9�{��&�P���T�:*���:�7��#YYYl �t��#a�p0��	�';��A%����~9��cA��AA�!Vg����M�5�(}��?wQclr�/����oAJ� �+p�I>9Hy[�ɮV8�x�t�3x%�6<���udG"3	�{v��32 �fH1�4�7��$m����9�L�;N����d�e�y@�|(��*2�uu8��;a��C��D"�ӄZ �8|'w'1�������V*�T���$�,z�0�_�Nβ���V)���&J�������*Pf@>��铺@�"����~k�g��v�8�QS��*��Ҥ2�����5�m�H>����׬>���o��Fsl5%@����Mnn��'F��9 v�J#YYY���H4��lH����Ռ]#YYY{<�U��s��#YYYI�#��YY��NHR�s{�偞�f���S����ހh��2z#����|BI�R�]��Fk�}�v��E���`#XXX�^�p���6#XXX&F��2���8�it�nbH+_fِI3�#y��F&���V8��j�uQ�`��f�����n����ܦh�Ϧ�n	�Iك�AZ��{�W�\"Q���c~�5�����V3��4ZV�o�|�K��F�4[ܹ�$��X&f���a1�!���Y/�z��9P����f�`���c���9�2B�������������)��K���k�#�������㏞w�I����1/u5�I�f�#XXXXbav�uy�� ��3T�&0F�ە�q�τ�S�,���9f�yr"`�å�t�	3C%CJ�9O�G'��,�T&�����6Jn�(�<��:E�~�X>@��L`?�v2��b�0��}�2"5P������ct��gY����ޑ� �QRm,X�Z8ª�g�?y0!#YYY�y�va��5��e���4av|��ib�t1T��Q�d�I�����8�9*y�����#XXX�~&�w�QŞ`v���`0O�óD�5N��7ԌgIZgf�c�)�����$C��Hѳ*0b1F)�qә4`�b�v������/+ެs���s�#YYY��f��w0G�c\����B��w�J������)�^�;[<,��nⅆ�aR���#YYYK�gݜ��V�C}�"b�9�&�1/`G���d!";V뢶/�6�ƢZ�Tj)	�S�қ=#YYY��cj=�Ù�ȶ�"z�Rb#��O����D�2���+�^�?-��Q�cYt��������o��틅�K�ض�z���1��?T$-���'� z ~c����J?'�T��w$S�	�*��
#<==

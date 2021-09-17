#!/usr/bin/env python
# Copyright 2014-2020 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

from pyscf import lib
from pyscf.tdscf import uks
from pyscf.pbc.tdscf.uhf import TDA
from pyscf.pbc.tdscf.uhf import TDHF as TDDFT

RPA = TDUKS = TDDFT


class TDDFTNoHybrid(uks.TDDFTNoHybrid):
    def gen_vind(self, mf):
        vind, hdiag = uks.TDDFTNoHybrid.gen_vind(self, mf)
        def vindp(x):
            with lib.temporary_env(mf, exxdiv=None):
                return vind(x)
        return vindp, hdiag

    def nuc_grad_method(self):
        raise NotImplementedError

def tddft(mf):
    '''Driver to create TDDFT or TDDFTNoHybrid object'''
    if mf._numint.libxc.is_hybrid_xc(mf.xc):
        return TDDFT(mf)
    else:
        return TDDFTNoHybrid(mf)

from pyscf.pbc import dft
dft.uks.UKS.TDA           = lib.class_as_method(TDA)
dft.uks.UKS.TDHF          = None
dft.uks.UKS.TDDFT         = tddft
#dft.rks.RKS.dTDA          = lib.class_as_method(dTDA)
#dft.rks.RKS.dRPA          = lib.class_as_method(dRPA)


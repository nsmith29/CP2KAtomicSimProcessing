import numpy as np
import math
import Core
import FromFile
import Graphics
import DataProcessing
from PySide6.QtGui import QVector3D
from PySide6.QtWidgets import *
from PySide6.QtDataVisualization import *

class WfnData():
    def __int__(self, suffix, subdir):
        print('in process')



    # def BondDetermination(self):
    #     for h in range(0, int(self.totatom)):
    #         bonds_formed = Graphics.atom_lookup(self.atoms[h]).identification()[-1]
    #
    #         exec(f'self.distance_from_atom{h} = []')
    #         exec(f'self.from_atom{h}_to_atom = []')
    #         exec(f'atom{h}_bonded_to = []')
    #         for f in range(0, int(self.totatom)):
    #             if h != f:
    #                 dis = np.sqrt(
    #                     (self.X[h] - self.X[f]) ** 2 + (self.Y[h] - self.Y[f]) ** 2 + (self.Z[h] - self.Z[f]) ** 2)
    #                 exec(f'self.distance_from_atom{h}.append(dis)')
    #                 exec(f'self.from_atom{h}_to_atom.append(f)')
    #
    #         closeness_to_atom = [x for _, x in sorted(
    #             zip(eval("self.distance_from_atom{}".format(h)), eval("self.from_atom{}_to_atom".format(h))))]
    #         for m in range(0, int(bonds_formed)):
    #             Atom = self.atoms[int(closeness_to_atom[m])]
    #             if Graphics.atom_lookup(Atom).identification()[-1] >= bonds_formed:
    #                 if self.atoms[h] != Atom:
    #                     F = eval("closeness_to_atom[{}]".format(m))
    #                     if str("{}".format(h)) in WfnData.BondsAlreadyMadeStore[str("{}".format(F))]:
    #                         break
    #                     else:
    #                         self.Bonds(h, F)




    # @classmethod
    # def addBondEntry(cls, h, f):
    #     H = str("{}".format(h))
    #     F = str("{}".format(f))
    #     WfnData.BondsAlreadyMadeStore[H][F] = length

    # def Bonds(self, h, F):
    #     xdiff = self.X[h] - self.X[F]
    #     ydiff = self.Y[h] - self.Y[F]
    #     zdiff = self.Z[h] - self.Z[F]
    #
    #
    #     self.addBondEntry(h, F)


    # def ScatterDataPoints(self):
    #     for Atom, index in zip(list(self.atoms), range(0, int(self.totatom))):
    #         for elem, i in zip(list(self.included_atoms), range(1, int(self.num_kind))):
    #             if Atom == elem:
    #                 x = float(self.X[index])
    #                 y = float(self.Y[index])
    #                 z = float(self.Z[index])
    #                 exec(f'self.data{i}{self.suffix}.setPosition(QVector3D(x, y, z))')
    #                 exec(f'self.series{i}{self.suffix}.dataProxy().addItem(self.data{i}{self.suffix})')
    #                 exec(f'self.series{i}{self.suffix}.setBaseColor(self.color{elem}{self.suffix})')
    #                 exec(f'self.series{i}{self.suffix}.setItemSize(float(self.size{elem}{self.suffix}))')


# class ScatterDataModifier:
#
#     def __init__(self, m_graph, series1, series2, series3, series4, series5, series6, series7, series8, series9, series10):
#         self.m_graph = m_graph
#
#         self.m_graph.activeTheme().setType(Q3DTheme.ThemeEbony)
#         self.m_graph.activeTheme().setBackgroundColor(QColor(Qt.black))
#         font = self.m_graph.activeTheme().font()
#         m_fontSize = 12
#         font.setPointSize(m_fontSize)
#         self.m_graph.activeTheme().setFont(font)
#         self.m_graph.setShadowQuality(QAbstract3DGraph.ShadowQualitySoftLow)
#         self.m_graph.scene().activeCamera().setCameraPreset(Q3DCamera.CameraPresetFront)
#         self.m_graph.scene().activeCamera().setMinZoomLevel(float(200.0))
#         self.m_graph_handler = Q3DInputHandler()
#         self.m_graph_handler.setRotationEnabled(True)
#         self.m_graph_handler.setZoomEnabled(True)
#         self.m_graph_handler.setSelectionEnabled(True)
#
#         proxy = QScatterDataProxy()
#         self.series = QScatter3DSeries(proxy)
#         self.series.setItemLabelFormat("@xTitle: @xLable @yTitle: @yLabel @zTitle: @zLabel")
#         self.m_smooth = True
#         self.series.setMeshSmooth(self.m_smooth)
#         self.m_graph.addSeries(self.series)
#
#         self.series1 = series1
#         self.series2 = series2
#         self.series3 = series3
#         self.series4 = series4
#         self.series5 = series5
#         self.series6 = series6
#         self.series7 = series7
#         self.series8 = series8
#         self.series9 = series9
#         self.series10 = series10
#
#         self.AddDataPoint()
#
#     def AddDataPoint(self):
#         self.m_graph.axisX().setTitle("X")
#         self.m_graph.axisY().setTitle("Y")
#         self.m_graph.axisZ().setTitle("Z")
#         self.m_graph.setAspectRatio(1.0)
#
#         self.m_graph.removeSeries(self.series)
#
#         self.series1.setItemLabelFormat("@xTitle: @xLabel @yTitle: @yLabel @zTitle: @zLabel")
#         self.m_graph.addSeries(self.series1)
#         if self.series2 != "None":
#             self.m_graph.addSeries(self.series2)
#         if self.series3 != "None":
#             self.m_graph.addSeries(self.series3)
#         if self.series4 != "None":
#             self.m_graph.addSeries(self.series4)
#         if self.series5 != "None":
#             self.m_graph.addSeries(self.series5)
#         if self.series6 != 'None':
#             self.m_graph.addSeries(self.series6)
#         if self.series7 != 'None':
#             self.m_graph.addSeries(self.series7)
#         if self.series8 != 'None':
#             self.m_graph.addSeries(self.series8)
#         if self.series9 != 'None':
#             self.m_graph.addSeries(self.series9)
#         if self.series10 != 'None':
#             self.m_graph.addSeries(self.series10)
#
#     def plotBonds(self, rpv, odi, baz, nsz, pzz, ahd, jun, lwc, kcx, xdd, utq, gnd, qsl, oyn, ybt, lxc, gpn, smc, ymd,
#                   emt, xhn, vtc, scw, zpp, mab, baa, rpm, qxh, ofw, svl, vrf, ilw, tgc, vnc, djd, hcd, gzx, pkp, bbm,
#                   nyn, vha, lpa, fsh, dce, voi, tpm, sqb, hsz, qjs, ngy, jte, aep, hmq, omd, rhd, lqd, apj, rft, txx, ytx,
#                   wve, dqy, rzg, tow, xla, hho, kmg, kxe, lii, yjc, jgq, ygj, jdk, ucq, fyt, zia, cxa, nnb, yde, fdm, rpc,
#                   rrl, sef, kbv, xag, wzx, run, vze, pcw, lki, szt, uko, qcz, cpz, skj, oeu, jst, zmj, wmg, psu, nvw, crg,
#                   zwy, nab, owy, guv, yyz, ohi, mse, lwm, syn, xkm, zih, gct, iap, vnb, oua, ebq, wjj, xkf, xri, ehm, irq,
#                   der, bhq, vwt, blc, ahr, prl, nhj, idd, yry, ciy, ypl, zth, avy, jky, wtq, bpi, ioe, jeo, gtu, epv, plw,
#                   guu, wks, wsp, zbo, exf, cyf, haj, zvx, ovq, bwr, zxd, llj, bjo, vva, fwu, xuz, cgh, gzs, rxw, ami, zib,
#                   ukm, xce, mgt, vfs, noo, kac, uul, eat, lvt, fsj, qur, hju, mcr, eze, cbr, jvl, foz, veg, pqg, qig, eut,
#                   fif, qoi, kti, vcn, mib, ivv, eob, eel, nma, ljp, kel, kfh, tqw, uoi, tza, eyg, kyi, dlt, ffp, knu, wtf,
#                   qtc, xnn, uzm, dvz, ifn, skf, ghc, lif, rdt, qwg, pbs, igo, ksi, sde, irk, ccs, adf, api, thi, rlm, rql,
#                   itk, eyo, tjt, bdc, ksy, qke, ulo, xyf, zxp, wqi, yav, ixt, rwe, hdp, bfh, wom, ozc, bkp, qhf, sib, vmj,
#                   exv, hom, zlf, lpw, sil, sko, scr, vba, krh, oxk, zek, atx, fss, trt, pee, vkr, ajn, woc, kiu, yyd, gga,
#                   lgl, jty, mjn, zxq, qzy, uxa, qir, lkn, aaq, ssg, wbl, ofe, yev, zin, toq, pwh, dad, ogz, mdl, zxe, ces,
#                   efs, pxy, odd, rdd, yjb, zsw, icn, qzw, epc, lck, wfi, xlo, ymo, eql, baf, qlf, yaf, rji, ahc, xiy, qzv,
#                   qif, xoh, rvb, vrz, fbs, shx, pea, ggr, ccm, tpi, thk, wfn, tup, qgj, pxo, zrs, sxb, gki, efk, giz, isl,
#                   qjk, pkv, rao, pxj, hxz, fxr, hdy, jqs, ewv, qcw, fdz, nad, qtd, vsg, tfw, zfe, jip, vwk, rty, vre, osl,
#                   aki, eja, eop, eea, nbx, uxz, qck, evw, lnv, llc, gnb, voa, cdb, cqv, kkp, ecx, ren, iri, kmf, pep, bpd,
#                   thu, yem, nac, ipi, jbx, owh, kwx, asc, sfj, mct, drb, tch, eko, tzq, iqj, tcn, cns, slk, cje, hsj, elp,
#                   xfs, sba, ocb, cnq, rnz, tcl, hxt, tmi, tiz, olz, qba, lgr, xhs, ear, ddp, sjq, gnr, omc, ldv, ecr, zmf,
#                   emi, tlj, ekt, enh, fkm, lmo, dqc, ovo, pqy, fqv, nmi, dcx, ypf, toa, ilc, ixo, kpn, nms, mhh, tpw, cpg,
#                   qmw, irz, fxv, nwr, inx, ojg, ojq, rcy, pwi, rcj, cfj, wkx, npk, ssj, inj, ika, mfe, sgv, hce, jso, kxi,
#                   coo, dxa, euy, lkk, jkd, kvo, dqz, hmy, pac, vhf, ohw, amv, sfo, wqc, mpf, rtg, fqo, qav, jqa, sdm, vyv,
#                   gba, qhb, dyd, pzq, wxz, jxy, cpw, rfj, kqo, lkb, pol, nyg, wau, ogo, lzw, jza, hqj, ivb, zlv, jgc, vda,
#                   gtk, aio, unl, nwe, xza, rjl, gue, xvo, eyc, blk, lzs, ibr, ndj, tld, fow, vun, voh, wns, otj, ahn, lhk,
#                   wpe, myq, ovs, yrt, ifx, dsc, jdw, wge, gnv, kfx, lgd, snv, iva, wkf, cjn, aay, rzt, aek, jtw, oye, vvz,
#                   qay, cjj, sxw, iyd, kio, tud, dmi, yqz, hyw, dex, oju, usw, hxh, mvc, pis, pnx, geu, xau, noc, oyd, lod,
#                   xyl, zmi, sob, axq, hbb, uaj, zln, pnj, ylk, ghr, nag, wnl, kxh, roc, ynv, pdk, bnc, cub, rbd, cgl, rtl,
#                   tln, xfu, aed, bwk, bmm, eqf, eoa, ahm, ayv, gbm, qkq, qkz, cyb, jmp, mcg, kkz, abg, sqz, ttz, voz, nis,
#                   vsw, aye, aya, vlz, pur, lnl, mpa, bee, xrx, gwq, bpb, kyp, mbb, fdr, ixh, xey, jhu, hvq, hgo, sjm, vyh,
#                   mbh, etr, vhy, ewc, lsx, uwb, cig, yyy, nwq, ixp, yqm, qaj, kyv, rln, lrd, tfe, kna, puq, vve, esf, tnf,
#                   kef, yqv, gtt, pou, fvc, eug, xqv, edk, yrg, emx, zkz, xgl, ssq, eoc, thw, ksf, bir, dcp, xll, axv, eqt,
#                   sbp, lmr, idn, vyt, ecw, iuo, nho, gdi, llp, mqd, fzv, xmf, iok, exr, upw, ita, bgl, mxb, ayf, xqz, tqv,
#                   fgd, dvg, dcj, dph, fak, zsy, syt, rgm, bmw, kia, zdx, jvq, lbs, uqh, bco, hoq, byh, myn, shk, khq, ttf,
#                   scm, qht, xae, mlb, xtq, cxq, agb, hvo, iec, xmy, qbl, xtg, kaz, bzx, zsl, gtn, afp, hvd, uen, ute, njv,
#                   lvx, zzj, exc, krr, hpd, tee, utf, rgz, ebc, rjh, rof, lum, uli, huk, rum, sog, mln, uok, mif, hwb, lfn,
#                   imc, vqj, mgm, hbi, pmb, aqr, myd, dcm, xgj, hvz, tyi, yhp, pfl, qpt, lvv, hyj, vlf, uzy, son, nze, tmn,
#                   zfw, sid, yov, unq, fqq, woy, fik, xbw, fwa, rqs, ehd, rza, ngj, pxi, moo, jrt, hni, fth, jyn, vef, hak,
#                   wlj, otv, nwk, jfq, pbw, ffd, trl, eje, chj, nen, pjs, uds, gaf, bsn, yhs, zvz, kqe, smb, ulc, hrc, rdb,
#                   ytf, fwy, jvu, tfy, sci, oxq, edj, eyd, wik, avc, che, qin, iwu, adb, ymt, hxl, yot, dud, omv, jus, qau,
#                   qwi, etw, con, kzn, bxc, kid, far, wpl, pgl, oaz, fgj, lqk, dct, brl, yxr, tcj, wrc, tof, lbz, sha, ghv,
#                   ljk, jxs, xfh, vrd, vej, nkm, jnr, qwj, dbp, orl, ypw, xxd, agt, sdr, oen, snx, mpp, ath, hyi, znb, otb,
#                   nfu, nyt, aen, tme, icb, gck, vpk, yub, vio, zfk, dte, mrs, xxt, fxo, lrk, qri, hoc, qvn, ibl, biu, zym,
#                   dyk, cmu, fix, nvo, dlm, zzm, iko, rmq, jmc, lsq, eyq, suf, kqb, swg, ium, voq, yzv, jbu, jcr, hym, cmg,
#                   evz, znn, fre, klv, ian, lsw, jod, kxk, swi, kgb, eis, qnc, usy, cmi, mjq, uie, inp, iuy, rnj, zzv, ulv,
#                   zqt, suo, zeq, huv, ldq, abm, ojp, myb, uyj, sbv, yif, fvi, rer, mem, dig, zew, sgk, erv, bxu, pns, ioo,
#                   jdo, aev, fxh, wxv, cnd, upg, vux, ken, wkw, ivm, oqm, qvx, ncx, pax, gkx, vrh, vsi, wnn, irs, igd, gwf,
#                   ldo, rfx, unv, heg, xtk, axk, rbz, gjd, xfj, opk, pwp, czh, nhq, wxf, wrw, nnz, riw, aui, lgx, tue, yly,
#                   uwj, cbv, aea, fav, hku, pvc, wei, gkz, pgv, yuc, iwh, xqo, ota, qew, dqg, bfg, ynz, exw, sud, vhj, ges,
#                   amw, iqt, kol, hfa, fvu, qsi, qix, tcr, ctk, qqg, wze, hod, hzr, nlh, qso, pja, oqe, rst, fzh, awz, atn,
#                   fwb, txd, ybg, tpe, how, nuu, wam, oiw, mrc, wjo, yfw, nxm, rqn, aju, eyh, xsj, zyp, hee, coj, xzj, uzf,
#                   sbb, wah, ldz, emu, umg, fpi, zpz, mzh, hqu, eoz, zxg, ncc, kbs, usi, hzi, rbh, kun, aoi, qwm, uyc, duh,
#                   eyn, gdh, lca, ubu, zsz, dns, xxn, zyg, cec, bla, unp, rjg, gti, qfc, nrj, hxf, ayh, hkg, akd, nfw, ouc,
#                   sul, isf, biq, zun, khc, xpj, grn, hut, bzo, zzl, wpu, ihi, syo, rsw, ivn, jcy, ivi, biy, jhc, izz, vlx,
#                   lyr, kmy, dsl, ptb, evn, ciw, kht, lmb, rpp, uln, yha, dhq, tkk, ayp, ija, rnd, ztc, fxl, sly, rig, xdh,
#                   xnz, ufa, ehv, zkv, jpm, jyb, jyu, ukn, qeh, yal, mlg, yup, puk, cof, bvl, gjv, stg, gjk, ofr, utn, sis,
#                   yjo, ewj, pdb, lac, ajp, esr, ovc, bcv, nqx, znq, utk, jmz, xwg, yfp, wkn, prm, elr, ile, xpy, tss, gei,
#                   jfy, qzl, siv, kyb, gil, kqv, gjq, vbj, gtl, cbk, ehw, eyf, fce, xsu, wzs, wbn, awa, tze, zvc, fnc, rda,
#                   tqe, hft, ctt, ufz, hjd, gsn, sgd, dji, wmx, qds, oiv, row, mhr, jql, noe, ohk, mdd, ocr, ltf, qrm, hou,
#                   tli, kuh, bnn, qzm, nvz, nug, klc, hwq, xmt, ozi, fog, dcq, abq, dio, pxv, ani, qwr, uyu, alv, sce, onu,
#                   zkd, hfc, mcc, dne, oak, uuz, deb, rod, mzf, jzb, zvh, nzu, nzs, aza, gch, zuh, whs, ugu, kuv, lqv, let,
#                   hvw, bov, yna, xzn, pvm, jdv, sls, sbr, nnd, vtb, fbk, csj, hqc, mrg, ozk, ctx, nvj, lrj, edx, lyd, bqe,
#                   laj, qlo, xfd, mkb, buw, bgd, lmc, gll, ywr, uei, bvk, iyb, urk, pmh, nzw, bmz, cmf, hzl, dr, tvq, csd,
#                   xns, inq, xzc, nmo, pql, ufl, nja, bya, cuj, ikp, zzh, tbc, jqz, hlu, mhc, bgv, xcc, sft, hlm, gxj, sqx,
#                   veq, bos, ddq, cuu, jbg, fkl, jhh, dov, koq, yze, xmi, cuf, yfy, lwb, pte, rks, omz, rws, bjg, uwl, zdm,
#                   xtm, asn, rzf, mzo, rqq, nbr, qxm, kdj, hrk, uhu, yge, ovy, mlr, jjx, qol, pgy, nej, hbq, odw, baw, gzw,
#                   yaj, xja, qni, dbl, clr, tyh, bah, elg, kda, ync, mzd, iku, tau, pzx, fsy, qmq, ugi, ods, fjk, zfv, ecp,
#                   ukb, rhn, wgg, vbo, zws, hpc, qdb, oaw, lcq, grc, vkb, oyz, bzk, lyh, dfp, wru, frg, izu, tqq, xlh, mes,
#                   svf, ipe, vyz, hgm, wyc, iwe, gow, cem, euv, pmu, qfk, qmp, zpm, ily, pbc, bhc, gwa, gbq, anq, msq, nkw,
#                   xfc, tmu, nqu, fkg, muv, uja, fjy, ppe, fpm, qob, acw, vyc, vzt, div, pcv, kmx, brn, qgf, wzu, dkm, srf,
#                   sdo, sby, rjw, eln, gxz, guq, gsw, fsb, vtp, cxp, nea, iaa, pez, mdm, slf, zfm, eak, cdm, ymi, eax, pfu,
#                   xui, jrr, jiy, prv, nml, mxy, wto, qoh, hvb, iqw, scj, qhs, moj, vtl, yxy, yak, nta, csv, yrl, vxi, fuf,
#                   krz, jvn, pnv, ezl, iau, aaj, xir, qdj, zel, jej, vds, jxq, ras, flw, lfw, uoj, ohu, lxy, vyf, znr, sox,
#                   ukw, meh, qmm, yef, zkn, het, zai, tmq, qyn, mws, rwb, aok, efp, qqi, qit, tfx, wxp, fjo, gtf, juo, bsh,
#                   gvt, cln, rzk, jsk, zyv, phn, pco, gsi, jri, tqs, mfh, yfm, cdi, zay, ecs, txv, ant, ay, aul, kwr, zqb,
#                   wqv, jtz, cds, luj, gal, hyf, jmi, npr, dwy, ehs, hfq, zcw, qnu, aer, pej, fru, mub, lkc, hjf, aab, eqx,
#                   rtd, byn, aoy, kat, kru, dkv, djw, ezm, syb, gbz, rhx, rge, ise, rev, xwi, xti, wxd, sli, dek, lgs, xkz,
#                   vpa, clv, haf, usu, mmo, ntc, kay, edr, iiv, duj, wtk, xdl, lwn, zrt, eol, kgc, zks, bad, cyd, ach, lox,
#                   dsw, yuh, zgp, iib, jkx, uwe, knh, chk, zgj, gka, asa, ioj, qak, jov, ynm, wdb, owe, uod, zjw, paj, txi,
#                   sab, mhu, oyc, rtc, akf, tzs, yba, grp, cdw, syx, mnv, xeh, hxo, kkk, dwr, zpn, pnl, bgb, ivs, rcg, orn,
#                   nwx, zrp, rmd, jnl, fvv, gyl, wgv, sqq, qzj, yve, kos, ece, igk, ybw, epa, lsb, nvl, lem, idi, fzm, agm,
#                   rja, vfc, emy, djk, pw, efq, zpl, iks, ypm, lme, jba, blt, aod, dkx, mey, rdm, tlz, ivw, rpa, dgz, zpa,
#                   kto, ltz, pfk, ema, tjo, jje, hzd, fxt, azp, zmc, gxl, qiw, plt, zhk, wpr, zrf, dwk, cwm, kyf, kfa, jnt,
#                   jjn, fii, mjl, vdt, uga, lff, omm, gyf, qhn, fpx, ksm, jyq, ilo, qbe, pxs, xup, srs, nzx, gda, yxq, cuc,
#                   rrv, kem, xbx, aug, sjg, rjb, ipt, qhh, bpm, sma, rex, aql, evp, lxm, zop, asm, twg, uak, bwh, uke, cpf,
#                   xcp, quv, tnq, awu, qud, lvw, kuf, eph, hxs, ifi, yag, tbj, gah, ybf, vnl, rgf, ezw, xul, vqb, xlt, edi,
#                   twn, krk, jcq, iez, ady, via, yiv, xyi, pif, ket, zzq, epi, mxq, vby, jpx, lru, rae, oiy, gam, ljf, gha,
#                   alb, duq, wyj, dck, rwc, qlk, niy, oxx, raz, bjm, hmw, uae, dnk, btz, wgt, eoh, sgh, gri, fgh, pvl, vhb,
#                   cfx, rkw, ezo, juu, erc, cyx, ewy, ylh, xwq, eri, jsa, llk, bec, uhc, xhh, phf, lvn, dca, vfz, nvc, nsw,
#                   waj, dqj, wnq, byw, ypi, ygg, njn, vxj, gvq, giv, wpt, bog, gzu, kcl, uco, guz, hby, axj, qve, vov, yfj,
#                   bph, wad, fpa, tnz, dbu, hyg, tav, vyl, ovr, juj, neb, zwi, mio, bhh, hqe, xga, tnp, fmx, ewo, mlh, bqk,
#                   kcb, htt, usp, oil, ttx, ajx, zac, jll, qrl, tkg, vrk, puu, kpw, qop, tkn, whe, juh, spn, tcf, xxj, ogu,
#                   ywz, mwx, lvm, vzx, due, cxr, sug, hhs, gbx, teu, tur, uju, hhf, dma, nsb, kdo, akr, gqd, kkg, uit, ibg,
#                   klu, vbx, get, jqr, zuz, zkh, ppp, vtd, kzd, vhn, nuj, paq, kwm, hyu, wae, zom, uth, mnb, gfl, uck, cwn,
#                   gjm, btk, tlr, exb, szr, odt, dwl, tez, qgs, etb, gqt, eqb, iyc, cux, nlt, tcs, qdl, zea, ufi, ugr, png,
#                   lbn, fye, gpb, atk, psz, reg, rzn, kiz):
#         if rpv !=  "None":
#            self.m_graph.addSeries(rpv)
#         if odi !=  "None":
#            self.m_graph.addSeries(odi)
#         if baz !=  "None":
#            self.m_graph.addSeries(baz)
#         if nsz !=  "None":
#            self.m_graph.addSeries(nsz)
#         if pzz !=  "None":
#            self.m_graph.addSeries(pzz)
#         if ahd !=  "None":
#            self.m_graph.addSeries(ahd)
#         if jun !=  "None":
#            self.m_graph.addSeries(jun)
#         if lwc !=  "None":
#            self.m_graph.addSeries(lwc)
#         if kcx !=  "None":
#            self.m_graph.addSeries(kcx)
#         if xdd !=  "None":
#            self.m_graph.addSeries(xdd)
#         if utq !=  "None":
#            self.m_graph.addSeries(utq)
#         if gnd !=  "None":
#            self.m_graph.addSeries(gnd)
#         if qsl !=  "None":
#            self.m_graph.addSeries(qsl)
#         if oyn !=  "None":
#            self.m_graph.addSeries(oyn)
#         if ybt !=  "None":
#            self.m_graph.addSeries(ybt)
#         if lxc !=  "None":
#            self.m_graph.addSeries(lxc)
#         if gpn !=  "None":
#            self.m_graph.addSeries(gpn)
#         if smc !=  "None":
#            self.m_graph.addSeries(smc)
#         if ymd !=  "None":
#            self.m_graph.addSeries(ymd)
#         if emt !=  "None":
#            self.m_graph.addSeries(emt)
#         if xhn !=  "None":
#            self.m_graph.addSeries(xhn)
#         if vtc !=  "None":
#            self.m_graph.addSeries(vtc)
#         if scw !=  "None":
#            self.m_graph.addSeries(scw)
#         if zpp !=  "None":
#            self.m_graph.addSeries(zpp)
#         if mab !=  "None":
#            self.m_graph.addSeries(mab)
#         if baa !=  "None":
#            self.m_graph.addSeries(baa)
#         if rpm !=  "None":
#            self.m_graph.addSeries(rpm)
#         if qxh !=  "None":
#            self.m_graph.addSeries(qxh)
#         if ofw !=  "None":
#            self.m_graph.addSeries(ofw)
#         if svl !=  "None":
#            self.m_graph.addSeries(svl)
#         if vrf !=  "None":
#            self.m_graph.addSeries(vrf)
#         if ilw !=  "None":
#            self.m_graph.addSeries(ilw)
#         if tgc !=  "None":
#            self.m_graph.addSeries(tgc)
#         if vnc !=  "None":
#            self.m_graph.addSeries(vnc)
#         if djd !=  "None":
#            self.m_graph.addSeries(djd)
#         if hcd !=  "None":
#            self.m_graph.addSeries(hcd)
#         if gzx !=  "None":
#            self.m_graph.addSeries(gzx)
#         if pkp !=  "None":
#            self.m_graph.addSeries(pkp)
#         if bbm !=  "None":
#            self.m_graph.addSeries(bbm)
#         if nyn !=  "None":
#            self.m_graph.addSeries(nyn)
#         if vha !=  "None":
#            self.m_graph.addSeries(vha)
#         if lpa !=  "None":
#            self.m_graph.addSeries(lpa)
#         if fsh !=  "None":
#            self.m_graph.addSeries(fsh)
#         if dce !=  "None":
#            self.m_graph.addSeries(dce)
#         if voi !=  "None":
#            self.m_graph.addSeries(voi)
#         if tpm !=  "None":
#            self.m_graph.addSeries(tpm)
#         if sqb !=  "None":
#            self.m_graph.addSeries(sqb)
#         if hsz !=  "None":
#            self.m_graph.addSeries(hsz)
#         if qjs !=  "None":
#            self.m_graph.addSeries(qjs)
#         if ngy !=  "None":
#            self.m_graph.addSeries(ngy)
#         if jte !=  "None":
#            self.m_graph.addSeries(jte)
#         if aep !=  "None":
#            self.m_graph.addSeries(aep)
#         if hmq !=  "None":
#            self.m_graph.addSeries(hmq)
#         if omd !=  "None":
#            self.m_graph.addSeries(omd)
#         if rhd !=  "None":
#            self.m_graph.addSeries(rhd)
#         if lqd !=  "None":
#            self.m_graph.addSeries(lqd)
#         if apj !=  "None":
#            self.m_graph.addSeries(apj)
#         if rft !=  "None":
#            self.m_graph.addSeries(rft)
#         if txx !=  "None":
#            self.m_graph.addSeries(txx)
#         if ytx !=  "None":
#            self.m_graph.addSeries(ytx)
#         if wve !=  "None":
#            self.m_graph.addSeries(wve)
#         if dqy !=  "None":
#            self.m_graph.addSeries(dqy)
#         if rzg !=  "None":
#            self.m_graph.addSeries(rzg)
#         if tow !=  "None":
#            self.m_graph.addSeries(tow)
#         if xla !=  "None":
#            self.m_graph.addSeries(xla)
#         if hho !=  "None":
#            self.m_graph.addSeries(hho)
#         if kmg !=  "None":
#            self.m_graph.addSeries(kmg)
#         if kxe !=  "None":
#            self.m_graph.addSeries(kxe)
#         if lii !=  "None":
#            self.m_graph.addSeries(lii)
#         if yjc !=  "None":
#            self.m_graph.addSeries(yjc)
#         if jgq !=  "None":
#            self.m_graph.addSeries(jgq)
#         if ygj !=  "None":
#            self.m_graph.addSeries(ygj)
#         if jdk !=  "None":
#            self.m_graph.addSeries(jdk)
#         if ucq !=  "None":
#            self.m_graph.addSeries(ucq)
#         if fyt !=  "None":
#            self.m_graph.addSeries(fyt)
#         if zia !=  "None":
#            self.m_graph.addSeries(zia)
#         if cxa !=  "None":
#            self.m_graph.addSeries(cxa)
#         if nnb !=  "None":
#            self.m_graph.addSeries(nnb)
#         if yde !=  "None":
#            self.m_graph.addSeries(yde)
#         if fdm !=  "None":
#            self.m_graph.addSeries(fdm)
#         if rpc !=  "None":
#            self.m_graph.addSeries(rpc)
#         if rrl !=  "None":
#            self.m_graph.addSeries(rrl)
#         if sef !=  "None":
#            self.m_graph.addSeries(sef)
#         if kbv !=  "None":
#            self.m_graph.addSeries(kbv)
#         if xag !=  "None":
#            self.m_graph.addSeries(xag)
#         if wzx !=  "None":
#            self.m_graph.addSeries(wzx)
#         if run !=  "None":
#            self.m_graph.addSeries(run)
#         if vze !=  "None":
#            self.m_graph.addSeries(vze)
#         if pcw !=  "None":
#            self.m_graph.addSeries(pcw)
#         if lki !=  "None":
#            self.m_graph.addSeries(lki)
#         if szt !=  "None":
#            self.m_graph.addSeries(szt)
#         if uko !=  "None":
#            self.m_graph.addSeries(uko)
#         if qcz !=  "None":
#            self.m_graph.addSeries(qcz)
#         if cpz !=  "None":
#            self.m_graph.addSeries(cpz)
#         if skj !=  "None":
#            self.m_graph.addSeries(skj)
#         if oeu !=  "None":
#            self.m_graph.addSeries(oeu)
#         if jst !=  "None":
#            self.m_graph.addSeries(jst)
#         if zmj !=  "None":
#            self.m_graph.addSeries(zmj)
#         if wmg !=  "None":
#            self.m_graph.addSeries(wmg)
#         if psu !=  "None":
#            self.m_graph.addSeries(psu)
#         if nvw !=  "None":
#            self.m_graph.addSeries(nvw)
#         if crg !=  "None":
#            self.m_graph.addSeries(crg)
#         if zwy !=  "None":
#            self.m_graph.addSeries(zwy)
#         if nab !=  "None":
#            self.m_graph.addSeries(nab)
#         if owy !=  "None":
#            self.m_graph.addSeries(owy)
#         if guv !=  "None":
#            self.m_graph.addSeries(guv)
#         if yyz !=  "None":
#            self.m_graph.addSeries(yyz)
#         if ohi !=  "None":
#            self.m_graph.addSeries(ohi)
#         if mse !=  "None":
#            self.m_graph.addSeries(mse)
#         if lwm !=  "None":
#            self.m_graph.addSeries(lwm)
#         if syn !=  "None":
#            self.m_graph.addSeries(syn)
#         if xkm !=  "None":
#            self.m_graph.addSeries(xkm)
#         if zih !=  "None":
#            self.m_graph.addSeries(zih)
#         if gct !=  "None":
#            self.m_graph.addSeries(gct)
#         if iap !=  "None":
#            self.m_graph.addSeries(iap)
#         if vnb !=  "None":
#            self.m_graph.addSeries(vnb)
#         if oua !=  "None":
#            self.m_graph.addSeries(oua)
#         if ebq !=  "None":
#            self.m_graph.addSeries(ebq)
#         if wjj !=  "None":
#            self.m_graph.addSeries(wjj)
#         if xkf !=  "None":
#            self.m_graph.addSeries(xkf)
#         if xri !=  "None":
#            self.m_graph.addSeries(xri)
#         if ehm !=  "None":
#            self.m_graph.addSeries(ehm)
#         if irq !=  "None":
#            self.m_graph.addSeries(irq)
#         if der !=  "None":
#            self.m_graph.addSeries(der)
#         if bhq !=  "None":
#            self.m_graph.addSeries(bhq)
#         if vwt !=  "None":
#            self.m_graph.addSeries(vwt)
#         if blc !=  "None":
#            self.m_graph.addSeries(blc)
#         if ahr !=  "None":
#            self.m_graph.addSeries(ahr)
#         if prl !=  "None":
#            self.m_graph.addSeries(prl)
#         if nhj !=  "None":
#            self.m_graph.addSeries(nhj)
#         if idd !=  "None":
#            self.m_graph.addSeries(idd)
#         if yry !=  "None":
#            self.m_graph.addSeries(yry)
#         if ciy !=  "None":
#            self.m_graph.addSeries(ciy)
#         if ypl !=  "None":
#            self.m_graph.addSeries(ypl)
#         if zth !=  "None":
#            self.m_graph.addSeries(zth)
#         if avy !=  "None":
#            self.m_graph.addSeries(avy)
#         if jky !=  "None":
#            self.m_graph.addSeries(jky)
#         if wtq !=  "None":
#            self.m_graph.addSeries(wtq)
#         if bpi !=  "None":
#            self.m_graph.addSeries(bpi)
#         if ioe !=  "None":
#            self.m_graph.addSeries(ioe)
#         if jeo !=  "None":
#            self.m_graph.addSeries(jeo)
#         if gtu !=  "None":
#            self.m_graph.addSeries(gtu)
#         if epv !=  "None":
#            self.m_graph.addSeries(epv)
#         if plw !=  "None":
#            self.m_graph.addSeries(plw)
#         if guu !=  "None":
#            self.m_graph.addSeries(guu)
#         if wks !=  "None":
#            self.m_graph.addSeries(wks)
#         if wsp !=  "None":
#            self.m_graph.addSeries(wsp)
#         if zbo !=  "None":
#            self.m_graph.addSeries(zbo)
#         if exf !=  "None":
#            self.m_graph.addSeries(exf)
#         if cyf !=  "None":
#            self.m_graph.addSeries(cyf)
#         if haj !=  "None":
#            self.m_graph.addSeries(haj)
#         if zvx !=  "None":
#            self.m_graph.addSeries(zvx)
#         if ovq !=  "None":
#            self.m_graph.addSeries(ovq)
#         if bwr !=  "None":
#            self.m_graph.addSeries(bwr)
#         if zxd !=  "None":
#            self.m_graph.addSeries(zxd)
#         if llj !=  "None":
#            self.m_graph.addSeries(llj)
#         if bjo !=  "None":
#            self.m_graph.addSeries(bjo)
#         if vva !=  "None":
#            self.m_graph.addSeries(vva)
#         if fwu !=  "None":
#            self.m_graph.addSeries(fwu)
#         if xuz !=  "None":
#            self.m_graph.addSeries(xuz)
#         if cgh !=  "None":
#            self.m_graph.addSeries(cgh)
#         if gzs !=  "None":
#            self.m_graph.addSeries(gzs)
#         if rxw !=  "None":
#            self.m_graph.addSeries(rxw)
#         if ami !=  "None":
#            self.m_graph.addSeries(ami)
#         if zib !=  "None":
#            self.m_graph.addSeries(zib)
#         if ukm !=  "None":
#            self.m_graph.addSeries(ukm)
#         if xce !=  "None":
#            self.m_graph.addSeries(xce)
#         if mgt !=  "None":
#            self.m_graph.addSeries(mgt)
#         if vfs !=  "None":
#            self.m_graph.addSeries(vfs)
#         if noo !=  "None":
#            self.m_graph.addSeries(noo)
#         if kac !=  "None":
#            self.m_graph.addSeries(kac)
#         if uul !=  "None":
#            self.m_graph.addSeries(uul)
#         if eat !=  "None":
#            self.m_graph.addSeries(eat)
#         if lvt !=  "None":
#            self.m_graph.addSeries(lvt)
#         if fsj !=  "None":
#            self.m_graph.addSeries(fsj)
#         if qur !=  "None":
#            self.m_graph.addSeries(qur)
#         if hju !=  "None":
#            self.m_graph.addSeries(hju)
#         if mcr !=  "None":
#            self.m_graph.addSeries(mcr)
#         if eze !=  "None":
#            self.m_graph.addSeries(eze)
#         if cbr !=  "None":
#            self.m_graph.addSeries(cbr)
#         if jvl !=  "None":
#            self.m_graph.addSeries(jvl)
#         if foz !=  "None":
#            self.m_graph.addSeries(foz)
#         if veg !=  "None":
#            self.m_graph.addSeries(veg)
#         if pqg !=  "None":
#            self.m_graph.addSeries(pqg)
#         if qig !=  "None":
#            self.m_graph.addSeries(qig)
#         if eut !=  "None":
#            self.m_graph.addSeries(eut)
#         if fif !=  "None":
#            self.m_graph.addSeries(fif)
#         if qoi !=  "None":
#            self.m_graph.addSeries(qoi)
#         if kti !=  "None":
#            self.m_graph.addSeries(kti)
#         if vcn !=  "None":
#            self.m_graph.addSeries(vcn)
#         if mib !=  "None":
#            self.m_graph.addSeries(mib)
#         if ivv !=  "None":
#            self.m_graph.addSeries(ivv)
#         if eob !=  "None":
#            self.m_graph.addSeries(eob)
#         if eel !=  "None":
#            self.m_graph.addSeries(eel)
#         if nma !=  "None":
#            self.m_graph.addSeries(nma)
#         if ljp !=  "None":
#            self.m_graph.addSeries(ljp)
#         if kel !=  "None":
#            self.m_graph.addSeries(kel)
#         if kfh !=  "None":
#            self.m_graph.addSeries(kfh)
#         if tqw !=  "None":
#            self.m_graph.addSeries(tqw)
#         if uoi !=  "None":
#            self.m_graph.addSeries(uoi)
#         if tza !=  "None":
#            self.m_graph.addSeries(tza)
#         if eyg !=  "None":
#            self.m_graph.addSeries(eyg)
#         if kyi !=  "None":
#            self.m_graph.addSeries(kyi)
#         if dlt !=  "None":
#            self.m_graph.addSeries(dlt)
#         if ffp !=  "None":
#            self.m_graph.addSeries(ffp)
#         if knu !=  "None":
#            self.m_graph.addSeries(knu)
#         if wtf !=  "None":
#            self.m_graph.addSeries(wtf)
#         if qtc !=  "None":
#            self.m_graph.addSeries(qtc)
#         if xnn !=  "None":
#            self.m_graph.addSeries(xnn)
#         if uzm !=  "None":
#            self.m_graph.addSeries(uzm)
#         if dvz !=  "None":
#            self.m_graph.addSeries(dvz)
#         if ifn !=  "None":
#            self.m_graph.addSeries(ifn)
#         if skf !=  "None":
#            self.m_graph.addSeries(skf)
#         if ghc !=  "None":
#            self.m_graph.addSeries(ghc)
#         if lif !=  "None":
#            self.m_graph.addSeries(lif)
#         if rdt !=  "None":
#            self.m_graph.addSeries(rdt)
#         if qwg !=  "None":
#            self.m_graph.addSeries(qwg)
#         if pbs !=  "None":
#            self.m_graph.addSeries(pbs)
#         if igo !=  "None":
#            self.m_graph.addSeries(igo)
#         if ksi !=  "None":
#            self.m_graph.addSeries(ksi)
#         if sde !=  "None":
#            self.m_graph.addSeries(sde)
#         if irk !=  "None":
#            self.m_graph.addSeries(irk)
#         if ccs !=  "None":
#            self.m_graph.addSeries(ccs)
#         if adf !=  "None":
#            self.m_graph.addSeries(adf)
#         if api !=  "None":
#            self.m_graph.addSeries(api)
#         if thi !=  "None":
#            self.m_graph.addSeries(thi)
#         if rlm !=  "None":
#            self.m_graph.addSeries(rlm)
#         if rql !=  "None":
#            self.m_graph.addSeries(rql)
#         if itk !=  "None":
#            self.m_graph.addSeries(itk)
#         if eyo !=  "None":
#            self.m_graph.addSeries(eyo)
#         if tjt !=  "None":
#            self.m_graph.addSeries(tjt)
#         if bdc !=  "None":
#            self.m_graph.addSeries(bdc)
#         if ksy !=  "None":
#            self.m_graph.addSeries(ksy)
#         if qke !=  "None":
#            self.m_graph.addSeries(qke)
#         if ulo !=  "None":
#            self.m_graph.addSeries(ulo)
#         if xyf !=  "None":
#            self.m_graph.addSeries(xyf)
#         if zxp !=  "None":
#            self.m_graph.addSeries(zxp)
#         if wqi !=  "None":
#            self.m_graph.addSeries(wqi)
#         if yav !=  "None":
#            self.m_graph.addSeries(yav)
#         if ixt !=  "None":
#            self.m_graph.addSeries(ixt)
#         if rwe !=  "None":
#            self.m_graph.addSeries(rwe)
#         if hdp !=  "None":
#            self.m_graph.addSeries(hdp)
#         if bfh !=  "None":
#            self.m_graph.addSeries(bfh)
#         if wom !=  "None":
#            self.m_graph.addSeries(wom)
#         if ozc !=  "None":
#            self.m_graph.addSeries(ozc)
#         if bkp !=  "None":
#            self.m_graph.addSeries(bkp)
#         if qhf !=  "None":
#            self.m_graph.addSeries(qhf)
#         if sib !=  "None":
#            self.m_graph.addSeries(sib)
#         if vmj !=  "None":
#            self.m_graph.addSeries(vmj)
#         if exv !=  "None":
#            self.m_graph.addSeries(exv)
#         if hom !=  "None":
#            self.m_graph.addSeries(hom)
#         if zlf !=  "None":
#            self.m_graph.addSeries(zlf)
#         if lpw !=  "None":
#            self.m_graph.addSeries(lpw)
#         if sil !=  "None":
#            self.m_graph.addSeries(sil)
#         if sko !=  "None":
#            self.m_graph.addSeries(sko)
#         if scr !=  "None":
#            self.m_graph.addSeries(scr)
#         if vba !=  "None":
#            self.m_graph.addSeries(vba)
#         if krh !=  "None":
#            self.m_graph.addSeries(krh)
#         if oxk !=  "None":
#            self.m_graph.addSeries(oxk)
#         if zek !=  "None":
#            self.m_graph.addSeries(zek)
#         if atx !=  "None":
#            self.m_graph.addSeries(atx)
#         if fss !=  "None":
#            self.m_graph.addSeries(fss)
#         if trt !=  "None":
#            self.m_graph.addSeries(trt)
#         if pee !=  "None":
#            self.m_graph.addSeries(pee)
#         if vkr !=  "None":
#            self.m_graph.addSeries(vkr)
#         if ajn !=  "None":
#            self.m_graph.addSeries(ajn)
#         if woc !=  "None":
#            self.m_graph.addSeries(woc)
#         if kiu !=  "None":
#            self.m_graph.addSeries(kiu)
#         if yyd !=  "None":
#            self.m_graph.addSeries(yyd)
#         if gga !=  "None":
#            self.m_graph.addSeries(gga)
#         if lgl !=  "None":
#            self.m_graph.addSeries(lgl)
#         if jty !=  "None":
#            self.m_graph.addSeries(jty)
#         if mjn !=  "None":
#            self.m_graph.addSeries(mjn)
#         if zxq !=  "None":
#            self.m_graph.addSeries(zxq)
#         if qzy !=  "None":
#            self.m_graph.addSeries(qzy)
#         if uxa !=  "None":
#            self.m_graph.addSeries(uxa)
#         if qir !=  "None":
#            self.m_graph.addSeries(qir)
#         if lkn !=  "None":
#            self.m_graph.addSeries(lkn)
#         if aaq !=  "None":
#            self.m_graph.addSeries(aaq)
#         if ssg !=  "None":
#            self.m_graph.addSeries(ssg)
#         if wbl !=  "None":
#            self.m_graph.addSeries(wbl)
#         if ofe !=  "None":
#            self.m_graph.addSeries(ofe)
#         if yev !=  "None":
#            self.m_graph.addSeries(yev)
#         if zin !=  "None":
#            self.m_graph.addSeries(zin)
#         if toq !=  "None":
#            self.m_graph.addSeries(toq)
#         if pwh !=  "None":
#            self.m_graph.addSeries(pwh)
#         if dad !=  "None":
#            self.m_graph.addSeries(dad)
#         if ogz !=  "None":
#            self.m_graph.addSeries(ogz)
#         if mdl !=  "None":
#            self.m_graph.addSeries(mdl)
#         if zxe !=  "None":
#            self.m_graph.addSeries(zxe)
#         if ces !=  "None":
#            self.m_graph.addSeries(ces)
#         if efs !=  "None":
#            self.m_graph.addSeries(efs)
#         if pxy !=  "None":
#            self.m_graph.addSeries(pxy)
#         if odd !=  "None":
#            self.m_graph.addSeries(odd)
#         if rdd !=  "None":
#            self.m_graph.addSeries(rdd)
#         if yjb !=  "None":
#            self.m_graph.addSeries(yjb)
#         if zsw !=  "None":
#            self.m_graph.addSeries(zsw)
#         if icn !=  "None":
#            self.m_graph.addSeries(icn)
#         if qzw !=  "None":
#            self.m_graph.addSeries(qzw)
#         if epc !=  "None":
#            self.m_graph.addSeries(epc)
#         if lck !=  "None":
#            self.m_graph.addSeries(lck)
#         if wfi !=  "None":
#            self.m_graph.addSeries(wfi)
#         if xlo !=  "None":
#            self.m_graph.addSeries(xlo)
#         if ymo !=  "None":
#            self.m_graph.addSeries(ymo)
#         if eql !=  "None":
#            self.m_graph.addSeries(eql)
#         if baf !=  "None":
#            self.m_graph.addSeries(baf)
#         if qlf !=  "None":
#            self.m_graph.addSeries(qlf)
#         if yaf !=  "None":
#            self.m_graph.addSeries(yaf)
#         if rji !=  "None":
#            self.m_graph.addSeries(rji)
#         if ahc !=  "None":
#            self.m_graph.addSeries(ahc)
#         if xiy !=  "None":
#            self.m_graph.addSeries(xiy)
#         if qzv !=  "None":
#            self.m_graph.addSeries(qzv)
#         if qif !=  "None":
#            self.m_graph.addSeries(qif)
#         if xoh !=  "None":
#            self.m_graph.addSeries(xoh)
#         if rvb !=  "None":
#            self.m_graph.addSeries(rvb)
#         if vrz !=  "None":
#            self.m_graph.addSeries(vrz)
#         if fbs !=  "None":
#            self.m_graph.addSeries(fbs)
#         if shx !=  "None":
#            self.m_graph.addSeries(shx)
#         if pea !=  "None":
#            self.m_graph.addSeries(pea)
#         if ggr !=  "None":
#            self.m_graph.addSeries(ggr)
#         if ccm !=  "None":
#            self.m_graph.addSeries(ccm)
#         if tpi !=  "None":
#            self.m_graph.addSeries(tpi)
#         if thk !=  "None":
#            self.m_graph.addSeries(thk)
#         if wfn !=  "None":
#            self.m_graph.addSeries(wfn)
#         if tup !=  "None":
#            self.m_graph.addSeries(tup)
#         if qgj !=  "None":
#            self.m_graph.addSeries(qgj)
#         if pxo !=  "None":
#            self.m_graph.addSeries(pxo)
#         if zrs !=  "None":
#            self.m_graph.addSeries(zrs)
#         if sxb !=  "None":
#            self.m_graph.addSeries(sxb)
#         if gki !=  "None":
#            self.m_graph.addSeries(gki)
#         if efk !=  "None":
#            self.m_graph.addSeries(efk)
#         if giz !=  "None":
#            self.m_graph.addSeries(giz)
#         if isl !=  "None":
#            self.m_graph.addSeries(isl)
#         if qjk !=  "None":
#            self.m_graph.addSeries(qjk)
#         if pkv !=  "None":
#            self.m_graph.addSeries(pkv)
#         if rao !=  "None":
#            self.m_graph.addSeries(rao)
#         if pxj !=  "None":
#            self.m_graph.addSeries(pxj)
#         if hxz !=  "None":
#            self.m_graph.addSeries(hxz)
#         if fxr !=  "None":
#            self.m_graph.addSeries(fxr)
#         if hdy !=  "None":
#            self.m_graph.addSeries(hdy)
#         if jqs !=  "None":
#            self.m_graph.addSeries(jqs)
#         if ewv !=  "None":
#            self.m_graph.addSeries(ewv)
#         if qcw !=  "None":
#            self.m_graph.addSeries(qcw)
#         if fdz !=  "None":
#            self.m_graph.addSeries(fdz)
#         if nad !=  "None":
#            self.m_graph.addSeries(nad)
#         if qtd !=  "None":
#            self.m_graph.addSeries(qtd)
#         if vsg !=  "None":
#            self.m_graph.addSeries(vsg)
#         if tfw !=  "None":
#            self.m_graph.addSeries(tfw)
#         if zfe !=  "None":
#            self.m_graph.addSeries(zfe)
#         if jip !=  "None":
#            self.m_graph.addSeries(jip)
#         if vwk !=  "None":
#            self.m_graph.addSeries(vwk)
#         if rty !=  "None":
#            self.m_graph.addSeries(rty)
#         if vre !=  "None":
#            self.m_graph.addSeries(vre)
#         if osl !=  "None":
#            self.m_graph.addSeries(osl)
#         if aki !=  "None":
#            self.m_graph.addSeries(aki)
#         if eja !=  "None":
#            self.m_graph.addSeries(eja)
#         if eop !=  "None":
#            self.m_graph.addSeries(eop)
#         if eea !=  "None":
#            self.m_graph.addSeries(eea)
#         if nbx !=  "None":
#            self.m_graph.addSeries(nbx)
#         if uxz !=  "None":
#            self.m_graph.addSeries(uxz)
#         if qck !=  "None":
#            self.m_graph.addSeries(qck)
#         if evw !=  "None":
#            self.m_graph.addSeries(evw)
#         if lnv !=  "None":
#            self.m_graph.addSeries(lnv)
#         if llc !=  "None":
#            self.m_graph.addSeries(llc)
#         if gnb !=  "None":
#            self.m_graph.addSeries(gnb)
#         if voa !=  "None":
#            self.m_graph.addSeries(voa)
#         if cdb !=  "None":
#            self.m_graph.addSeries(cdb)
#         if cqv !=  "None":
#            self.m_graph.addSeries(cqv)
#         if kkp !=  "None":
#            self.m_graph.addSeries(kkp)
#         if ecx !=  "None":
#            self.m_graph.addSeries(ecx)
#         if ren !=  "None":
#            self.m_graph.addSeries(ren)
#         if iri !=  "None":
#            self.m_graph.addSeries(iri)
#         if kmf !=  "None":
#            self.m_graph.addSeries(kmf)
#         if pep !=  "None":
#            self.m_graph.addSeries(pep)
#         if bpd !=  "None":
#            self.m_graph.addSeries(bpd)
#         if thu !=  "None":
#            self.m_graph.addSeries(thu)
#         if yem !=  "None":
#            self.m_graph.addSeries(yem)
#         if nac !=  "None":
#            self.m_graph.addSeries(nac)
#         if ipi !=  "None":
#            self.m_graph.addSeries(ipi)
#         if jbx !=  "None":
#            self.m_graph.addSeries(jbx)
#         if owh !=  "None":
#            self.m_graph.addSeries(owh)
#         if kwx !=  "None":
#            self.m_graph.addSeries(kwx)
#         if asc !=  "None":
#            self.m_graph.addSeries(asc)
#         if sfj !=  "None":
#            self.m_graph.addSeries(sfj)
#         if mct !=  "None":
#            self.m_graph.addSeries(mct)
#         if drb !=  "None":
#            self.m_graph.addSeries(drb)
#         if tch !=  "None":
#            self.m_graph.addSeries(tch)
#         if eko !=  "None":
#            self.m_graph.addSeries(eko)
#         if tzq !=  "None":
#            self.m_graph.addSeries(tzq)
#         if iqj !=  "None":
#            self.m_graph.addSeries(iqj)
#         if tcn !=  "None":
#            self.m_graph.addSeries(tcn)
#         if cns !=  "None":
#            self.m_graph.addSeries(cns)
#         if slk !=  "None":
#            self.m_graph.addSeries(slk)
#         if cje !=  "None":
#            self.m_graph.addSeries(cje)
#         if hsj !=  "None":
#            self.m_graph.addSeries(hsj)
#         if elp !=  "None":
#            self.m_graph.addSeries(elp)
#         if xfs !=  "None":
#            self.m_graph.addSeries(xfs)
#         if sba !=  "None":
#            self.m_graph.addSeries(sba)
#         if ocb !=  "None":
#            self.m_graph.addSeries(ocb)
#         if cnq !=  "None":
#            self.m_graph.addSeries(cnq)
#         if rnz !=  "None":
#            self.m_graph.addSeries(rnz)
#         if tcl !=  "None":
#            self.m_graph.addSeries(tcl)
#         if hxt !=  "None":
#            self.m_graph.addSeries(hxt)
#         if tmi !=  "None":
#            self.m_graph.addSeries(tmi)
#         if tiz !=  "None":
#            self.m_graph.addSeries(tiz)
#         if olz !=  "None":
#            self.m_graph.addSeries(olz)
#         if qba !=  "None":
#            self.m_graph.addSeries(qba)
#         if lgr !=  "None":
#            self.m_graph.addSeries(lgr)
#         if xhs !=  "None":
#            self.m_graph.addSeries(xhs)
#         if ear !=  "None":
#            self.m_graph.addSeries(ear)
#         if ddp !=  "None":
#            self.m_graph.addSeries(ddp)
#         if sjq !=  "None":
#            self.m_graph.addSeries(sjq)
#         if gnr !=  "None":
#            self.m_graph.addSeries(gnr)
#         if omc !=  "None":
#            self.m_graph.addSeries(omc)
#         if ldv !=  "None":
#            self.m_graph.addSeries(ldv)
#         if ecr !=  "None":
#            self.m_graph.addSeries(ecr)
#         if zmf !=  "None":
#            self.m_graph.addSeries(zmf)
#         if emi !=  "None":
#            self.m_graph.addSeries(emi)
#         if tlj !=  "None":
#            self.m_graph.addSeries(tlj)
#         if ekt !=  "None":
#            self.m_graph.addSeries(ekt)
#         if enh !=  "None":
#            self.m_graph.addSeries(enh)
#         if fkm !=  "None":
#            self.m_graph.addSeries(fkm)
#         if lmo !=  "None":
#            self.m_graph.addSeries(lmo)
#         if dqc !=  "None":
#            self.m_graph.addSeries(dqc)
#         if ovo !=  "None":
#            self.m_graph.addSeries(ovo)
#         if pqy !=  "None":
#            self.m_graph.addSeries(pqy)
#         if fqv !=  "None":
#            self.m_graph.addSeries(fqv)
#         if nmi !=  "None":
#            self.m_graph.addSeries(nmi)
#         if dcx !=  "None":
#            self.m_graph.addSeries(dcx)
#         if ypf !=  "None":
#            self.m_graph.addSeries(ypf)
#         if toa !=  "None":
#            self.m_graph.addSeries(toa)
#         if ilc !=  "None":
#            self.m_graph.addSeries(ilc)
#         if ixo !=  "None":
#            self.m_graph.addSeries(ixo)
#         if kpn !=  "None":
#            self.m_graph.addSeries(kpn)
#         if nms !=  "None":
#            self.m_graph.addSeries(nms)
#         if mhh !=  "None":
#            self.m_graph.addSeries(mhh)
#         if tpw !=  "None":
#            self.m_graph.addSeries(tpw)
#         if cpg !=  "None":
#            self.m_graph.addSeries(cpg)
#         if qmw !=  "None":
#            self.m_graph.addSeries(qmw)
#         if irz !=  "None":
#            self.m_graph.addSeries(irz)
#         if fxv !=  "None":
#            self.m_graph.addSeries(fxv)
#         if nwr !=  "None":
#            self.m_graph.addSeries(nwr)
#         if inx !=  "None":
#            self.m_graph.addSeries(inx)
#         if ojg !=  "None":
#            self.m_graph.addSeries(ojg)
#         if ojq !=  "None":
#            self.m_graph.addSeries(ojq)
#         if rcy !=  "None":
#            self.m_graph.addSeries(rcy)
#         if pwi !=  "None":
#            self.m_graph.addSeries(pwi)
#         if rcj !=  "None":
#            self.m_graph.addSeries(rcj)
#         if cfj !=  "None":
#            self.m_graph.addSeries(cfj)
#         if wkx !=  "None":
#            self.m_graph.addSeries(wkx)
#         if npk !=  "None":
#            self.m_graph.addSeries(npk)
#         if ssj !=  "None":
#            self.m_graph.addSeries(ssj)
#         if inj !=  "None":
#            self.m_graph.addSeries(inj)
#         if ika !=  "None":
#            self.m_graph.addSeries(ika)
#         if mfe !=  "None":
#            self.m_graph.addSeries(mfe)
#         if sgv !=  "None":
#            self.m_graph.addSeries(sgv)
#         if hce !=  "None":
#            self.m_graph.addSeries(hce)
#         if jso !=  "None":
#            self.m_graph.addSeries(jso)
#         if kxi !=  "None":
#            self.m_graph.addSeries(kxi)
#         if coo !=  "None":
#            self.m_graph.addSeries(coo)
#         if dxa !=  "None":
#            self.m_graph.addSeries(dxa)
#         if euy !=  "None":
#            self.m_graph.addSeries(euy)
#         if lkk !=  "None":
#            self.m_graph.addSeries(lkk)
#         if jkd !=  "None":
#            self.m_graph.addSeries(jkd)
#         if kvo !=  "None":
#            self.m_graph.addSeries(kvo)
#         if dqz !=  "None":
#            self.m_graph.addSeries(dqz)
#         if hmy !=  "None":
#            self.m_graph.addSeries(hmy)
#         if pac !=  "None":
#            self.m_graph.addSeries(pac)
#         if vhf !=  "None":
#            self.m_graph.addSeries(vhf)
#         if ohw !=  "None":
#            self.m_graph.addSeries(ohw)
#         if amv !=  "None":
#            self.m_graph.addSeries(amv)
#         if sfo !=  "None":
#            self.m_graph.addSeries(sfo)
#         if wqc !=  "None":
#            self.m_graph.addSeries(wqc)
#         if mpf !=  "None":
#            self.m_graph.addSeries(mpf)
#         if rtg !=  "None":
#            self.m_graph.addSeries(rtg)
#         if fqo !=  "None":
#            self.m_graph.addSeries(fqo)
#         if qav !=  "None":
#            self.m_graph.addSeries(qav)
#         if jqa !=  "None":
#            self.m_graph.addSeries(jqa)
#         if sdm !=  "None":
#            self.m_graph.addSeries(sdm)
#         if vyv !=  "None":
#            self.m_graph.addSeries(vyv)
#         if gba !=  "None":
#            self.m_graph.addSeries(gba)
#         if qhb !=  "None":
#            self.m_graph.addSeries(qhb)
#         if dyd !=  "None":
#            self.m_graph.addSeries(dyd)
#         if pzq !=  "None":
#            self.m_graph.addSeries(pzq)
#         if wxz !=  "None":
#            self.m_graph.addSeries(wxz)
#         if jxy !=  "None":
#            self.m_graph.addSeries(jxy)
#         if cpw !=  "None":
#            self.m_graph.addSeries(cpw)
#         if rfj !=  "None":
#            self.m_graph.addSeries(rfj)
#         if kqo !=  "None":
#            self.m_graph.addSeries(kqo)
#         if lkb !=  "None":
#            self.m_graph.addSeries(lkb)
#         if pol !=  "None":
#            self.m_graph.addSeries(pol)
#         if nyg !=  "None":
#            self.m_graph.addSeries(nyg)
#         if wau !=  "None":
#            self.m_graph.addSeries(wau)
#         if ogo !=  "None":
#            self.m_graph.addSeries(ogo)
#         if lzw !=  "None":
#            self.m_graph.addSeries(lzw)
#         if jza !=  "None":
#            self.m_graph.addSeries(jza)
#         if hqj !=  "None":
#            self.m_graph.addSeries(hqj)
#         if ivb !=  "None":
#            self.m_graph.addSeries(ivb)
#         if zlv !=  "None":
#            self.m_graph.addSeries(zlv)
#         if jgc !=  "None":
#            self.m_graph.addSeries(jgc)
#         if vda !=  "None":
#            self.m_graph.addSeries(vda)
#         if gtk !=  "None":
#            self.m_graph.addSeries(gtk)
#         if aio !=  "None":
#            self.m_graph.addSeries(aio)
#         if unl !=  "None":
#            self.m_graph.addSeries(unl)
#         if nwe !=  "None":
#            self.m_graph.addSeries(nwe)
#         if xza !=  "None":
#            self.m_graph.addSeries(xza)
#         if rjl !=  "None":
#            self.m_graph.addSeries(rjl)
#         if gue !=  "None":
#            self.m_graph.addSeries(gue)
#         if xvo !=  "None":
#            self.m_graph.addSeries(xvo)
#         if eyc !=  "None":
#            self.m_graph.addSeries(eyc)
#         if blk !=  "None":
#            self.m_graph.addSeries(blk)
#         if lzs !=  "None":
#            self.m_graph.addSeries(lzs)
#         if ibr !=  "None":
#            self.m_graph.addSeries(ibr)
#         if ndj !=  "None":
#            self.m_graph.addSeries(ndj)
#         if tld !=  "None":
#            self.m_graph.addSeries(tld)
#         if fow !=  "None":
#            self.m_graph.addSeries(fow)
#         if vun !=  "None":
#            self.m_graph.addSeries(vun)
#         if voh !=  "None":
#            self.m_graph.addSeries(voh)
#         if wns !=  "None":
#            self.m_graph.addSeries(wns)
#         if otj !=  "None":
#            self.m_graph.addSeries(otj)
#         if ahn !=  "None":
#            self.m_graph.addSeries(ahn)
#         if lhk !=  "None":
#            self.m_graph.addSeries(lhk)
#         if wpe !=  "None":
#            self.m_graph.addSeries(wpe)
#         if myq !=  "None":
#            self.m_graph.addSeries(myq)
#         if ovs !=  "None":
#            self.m_graph.addSeries(ovs)
#         if yrt !=  "None":
#            self.m_graph.addSeries(yrt)
#         if ifx !=  "None":
#            self.m_graph.addSeries(ifx)
#         if dsc !=  "None":
#            self.m_graph.addSeries(dsc)
#         if jdw !=  "None":
#            self.m_graph.addSeries(jdw)
#         if wge !=  "None":
#            self.m_graph.addSeries(wge)
#         if gnv !=  "None":
#            self.m_graph.addSeries(gnv)
#         if kfx !=  "None":
#            self.m_graph.addSeries(kfx)
#         if lgd !=  "None":
#            self.m_graph.addSeries(lgd)
#         if snv !=  "None":
#            self.m_graph.addSeries(snv)
#         if iva !=  "None":
#            self.m_graph.addSeries(iva)
#         if wkf !=  "None":
#            self.m_graph.addSeries(wkf)
#         if cjn !=  "None":
#            self.m_graph.addSeries(cjn)
#         if aay !=  "None":
#            self.m_graph.addSeries(aay)
#         if rzt !=  "None":
#            self.m_graph.addSeries(rzt)
#         if aek !=  "None":
#            self.m_graph.addSeries(aek)
#         if jtw !=  "None":
#            self.m_graph.addSeries(jtw)
#         if oye !=  "None":
#            self.m_graph.addSeries(oye)
#         if vvz !=  "None":
#            self.m_graph.addSeries(vvz)
#         if qay !=  "None":
#            self.m_graph.addSeries(qay)
#         if cjj !=  "None":
#            self.m_graph.addSeries(cjj)
#         if sxw !=  "None":
#            self.m_graph.addSeries(sxw)
#         if iyd !=  "None":
#            self.m_graph.addSeries(iyd)
#         if kio !=  "None":
#            self.m_graph.addSeries(kio)
#         if tud !=  "None":
#            self.m_graph.addSeries(tud)
#         if dmi !=  "None":
#            self.m_graph.addSeries(dmi)
#         if yqz !=  "None":
#            self.m_graph.addSeries(yqz)
#         if hyw !=  "None":
#            self.m_graph.addSeries(hyw)
#         if dex !=  "None":
#            self.m_graph.addSeries(dex)
#         if oju !=  "None":
#            self.m_graph.addSeries(oju)
#         if usw !=  "None":
#            self.m_graph.addSeries(usw)
#         if hxh !=  "None":
#            self.m_graph.addSeries(hxh)
#         if mvc !=  "None":
#            self.m_graph.addSeries(mvc)
#         if pis !=  "None":
#            self.m_graph.addSeries(pis)
#         if pnx !=  "None":
#            self.m_graph.addSeries(pnx)
#         if geu !=  "None":
#            self.m_graph.addSeries(geu)
#         if xau !=  "None":
#            self.m_graph.addSeries(xau)
#         if noc !=  "None":
#            self.m_graph.addSeries(noc)
#         if oyd !=  "None":
#            self.m_graph.addSeries(oyd)
#         if lod !=  "None":
#            self.m_graph.addSeries(lod)
#         if xyl !=  "None":
#            self.m_graph.addSeries(xyl)
#         if zmi !=  "None":
#            self.m_graph.addSeries(zmi)
#         if sob !=  "None":
#            self.m_graph.addSeries(sob)
#         if axq !=  "None":
#            self.m_graph.addSeries(axq)
#         if hbb !=  "None":
#            self.m_graph.addSeries(hbb)
#         if uaj !=  "None":
#            self.m_graph.addSeries(uaj)
#         if zln !=  "None":
#            self.m_graph.addSeries(zln)
#         if pnj !=  "None":
#            self.m_graph.addSeries(pnj)
#         if ylk !=  "None":
#            self.m_graph.addSeries(ylk)
#         if ghr !=  "None":
#            self.m_graph.addSeries(ghr)
#         if nag !=  "None":
#            self.m_graph.addSeries(nag)
#         if wnl !=  "None":
#            self.m_graph.addSeries(wnl)
#         if kxh !=  "None":
#            self.m_graph.addSeries(kxh)
#         if roc !=  "None":
#            self.m_graph.addSeries(roc)
#         if ynv !=  "None":
#            self.m_graph.addSeries(ynv)
#         if pdk !=  "None":
#            self.m_graph.addSeries(pdk)
#         if bnc !=  "None":
#            self.m_graph.addSeries(bnc)
#         if cub !=  "None":
#            self.m_graph.addSeries(cub)
#         if rbd !=  "None":
#            self.m_graph.addSeries(rbd)
#         if cgl !=  "None":
#            self.m_graph.addSeries(cgl)
#         if rtl !=  "None":
#            self.m_graph.addSeries(rtl)
#         if tln !=  "None":
#            self.m_graph.addSeries(tln)
#         if xfu !=  "None":
#            self.m_graph.addSeries(xfu)
#         if aed !=  "None":
#            self.m_graph.addSeries(aed)
#         if bwk !=  "None":
#            self.m_graph.addSeries(bwk)
#         if bmm !=  "None":
#            self.m_graph.addSeries(bmm)
#         if eqf !=  "None":
#            self.m_graph.addSeries(eqf)
#         if eoa !=  "None":
#            self.m_graph.addSeries(eoa)
#         if ahm !=  "None":
#            self.m_graph.addSeries(ahm)
#         if ayv !=  "None":
#            self.m_graph.addSeries(ayv)
#         if gbm !=  "None":
#            self.m_graph.addSeries(gbm)
#         if qkq !=  "None":
#            self.m_graph.addSeries(qkq)
#         if qkz !=  "None":
#            self.m_graph.addSeries(qkz)
#         if cyb !=  "None":
#            self.m_graph.addSeries(cyb)
#         if jmp !=  "None":
#            self.m_graph.addSeries(jmp)
#         if mcg !=  "None":
#            self.m_graph.addSeries(mcg)
#         if kkz !=  "None":
#            self.m_graph.addSeries(kkz)
#         if abg !=  "None":
#            self.m_graph.addSeries(abg)
#         if sqz !=  "None":
#            self.m_graph.addSeries(sqz)
#         if ttz !=  "None":
#            self.m_graph.addSeries(ttz)
#         if voz !=  "None":
#            self.m_graph.addSeries(voz)
#         if nis !=  "None":
#            self.m_graph.addSeries(nis)
#         if vsw !=  "None":
#            self.m_graph.addSeries(vsw)
#         if aye !=  "None":
#            self.m_graph.addSeries(aye)
#         if aya !=  "None":
#            self.m_graph.addSeries(aya)
#         if vlz !=  "None":
#            self.m_graph.addSeries(vlz)
#         if pur !=  "None":
#            self.m_graph.addSeries(pur)
#         if lnl !=  "None":
#            self.m_graph.addSeries(lnl)
#         if mpa !=  "None":
#            self.m_graph.addSeries(mpa)
#         if bee !=  "None":
#            self.m_graph.addSeries(bee)
#         if xrx !=  "None":
#            self.m_graph.addSeries(xrx)
#         if gwq !=  "None":
#            self.m_graph.addSeries(gwq)
#         if bpb !=  "None":
#            self.m_graph.addSeries(bpb)
#         if kyp !=  "None":
#            self.m_graph.addSeries(kyp)
#         if mbb !=  "None":
#            self.m_graph.addSeries(mbb)
#         if fdr !=  "None":
#            self.m_graph.addSeries(fdr)
#         if ixh !=  "None":
#            self.m_graph.addSeries(ixh)
#         if xey !=  "None":
#            self.m_graph.addSeries(xey)
#         if jhu !=  "None":
#            self.m_graph.addSeries(jhu)
#         if hvq !=  "None":
#            self.m_graph.addSeries(hvq)
#         if hgo !=  "None":
#            self.m_graph.addSeries(hgo)
#         if sjm !=  "None":
#            self.m_graph.addSeries(sjm)
#         if vyh !=  "None":
#            self.m_graph.addSeries(vyh)
#         if mbh !=  "None":
#            self.m_graph.addSeries(mbh)
#         if etr !=  "None":
#            self.m_graph.addSeries(etr)
#         if vhy !=  "None":
#            self.m_graph.addSeries(vhy)
#         if ewc !=  "None":
#            self.m_graph.addSeries(ewc)
#         if lsx !=  "None":
#            self.m_graph.addSeries(lsx)
#         if uwb !=  "None":
#            self.m_graph.addSeries(uwb)
#         if cig !=  "None":
#            self.m_graph.addSeries(cig)
#         if yyy !=  "None":
#            self.m_graph.addSeries(yyy)
#         if nwq !=  "None":
#            self.m_graph.addSeries(nwq)
#         if ixp !=  "None":
#            self.m_graph.addSeries(ixp)
#         if yqm !=  "None":
#            self.m_graph.addSeries(yqm)
#         if qaj !=  "None":
#            self.m_graph.addSeries(qaj)
#         if kyv !=  "None":
#            self.m_graph.addSeries(kyv)
#         if rln !=  "None":
#            self.m_graph.addSeries(rln)
#         if lrd !=  "None":
#            self.m_graph.addSeries(lrd)
#         if tfe !=  "None":
#            self.m_graph.addSeries(tfe)
#         if kna !=  "None":
#            self.m_graph.addSeries(kna)
#         if puq !=  "None":
#            self.m_graph.addSeries(puq)
#         if vve !=  "None":
#            self.m_graph.addSeries(vve)
#         if esf !=  "None":
#            self.m_graph.addSeries(esf)
#         if tnf !=  "None":
#            self.m_graph.addSeries(tnf)
#         if kef !=  "None":
#            self.m_graph.addSeries(kef)
#         if yqv !=  "None":
#            self.m_graph.addSeries(yqv)
#         if gtt !=  "None":
#            self.m_graph.addSeries(gtt)
#         if pou !=  "None":
#            self.m_graph.addSeries(pou)
#         if fvc !=  "None":
#            self.m_graph.addSeries(fvc)
#         if eug !=  "None":
#            self.m_graph.addSeries(eug)
#         if xqv !=  "None":
#            self.m_graph.addSeries(xqv)
#         if edk !=  "None":
#            self.m_graph.addSeries(edk)
#         if yrg !=  "None":
#            self.m_graph.addSeries(yrg)
#         if emx !=  "None":
#            self.m_graph.addSeries(emx)
#         if zkz !=  "None":
#            self.m_graph.addSeries(zkz)
#         if xgl !=  "None":
#            self.m_graph.addSeries(xgl)
#         if ssq !=  "None":
#            self.m_graph.addSeries(ssq)
#         if eoc !=  "None":
#            self.m_graph.addSeries(eoc)
#         if thw !=  "None":
#            self.m_graph.addSeries(thw)
#         if ksf !=  "None":
#            self.m_graph.addSeries(ksf)
#         if bir !=  "None":
#            self.m_graph.addSeries(bir)
#         if dcp !=  "None":
#            self.m_graph.addSeries(dcp)
#         if xll !=  "None":
#            self.m_graph.addSeries(xll)
#         if axv !=  "None":
#            self.m_graph.addSeries(axv)
#         if eqt !=  "None":
#            self.m_graph.addSeries(eqt)
#         if sbp !=  "None":
#            self.m_graph.addSeries(sbp)
#         if lmr !=  "None":
#            self.m_graph.addSeries(lmr)
#         if idn !=  "None":
#            self.m_graph.addSeries(idn)
#         if vyt !=  "None":
#            self.m_graph.addSeries(vyt)
#         if ecw !=  "None":
#            self.m_graph.addSeries(ecw)
#         if iuo !=  "None":
#            self.m_graph.addSeries(iuo)
#         if nho !=  "None":
#            self.m_graph.addSeries(nho)
#         if gdi !=  "None":
#            self.m_graph.addSeries(gdi)
#         if llp !=  "None":
#            self.m_graph.addSeries(llp)
#         if mqd !=  "None":
#            self.m_graph.addSeries(mqd)
#         if fzv !=  "None":
#            self.m_graph.addSeries(fzv)
#         if xmf !=  "None":
#            self.m_graph.addSeries(xmf)
#         if iok !=  "None":
#            self.m_graph.addSeries(iok)
#         if exr !=  "None":
#            self.m_graph.addSeries(exr)
#         if upw !=  "None":
#            self.m_graph.addSeries(upw)
#         if ita !=  "None":
#            self.m_graph.addSeries(ita)
#         if bgl !=  "None":
#            self.m_graph.addSeries(bgl)
#         if mxb !=  "None":
#            self.m_graph.addSeries(mxb)
#         if ayf !=  "None":
#            self.m_graph.addSeries(ayf)
#         if xqz !=  "None":
#            self.m_graph.addSeries(xqz)
#         if tqv !=  "None":
#            self.m_graph.addSeries(tqv)
#         if fgd !=  "None":
#            self.m_graph.addSeries(fgd)
#         if dvg !=  "None":
#            self.m_graph.addSeries(dvg)
#         if dcj !=  "None":
#            self.m_graph.addSeries(dcj)
#         if dph !=  "None":
#            self.m_graph.addSeries(dph)
#         if fak !=  "None":
#            self.m_graph.addSeries(fak)
#         if zsy !=  "None":
#            self.m_graph.addSeries(zsy)
#         if syt !=  "None":
#            self.m_graph.addSeries(syt)
#         if rgm !=  "None":
#            self.m_graph.addSeries(rgm)
#         if bmw !=  "None":
#            self.m_graph.addSeries(bmw)
#         if kia !=  "None":
#            self.m_graph.addSeries(kia)
#         if zdx !=  "None":
#            self.m_graph.addSeries(zdx)
#         if jvq !=  "None":
#            self.m_graph.addSeries(jvq)
#         if lbs !=  "None":
#            self.m_graph.addSeries(lbs)
#         if uqh !=  "None":
#            self.m_graph.addSeries(uqh)
#         if bco !=  "None":
#            self.m_graph.addSeries(bco)
#         if hoq !=  "None":
#            self.m_graph.addSeries(hoq)
#         if byh !=  "None":
#            self.m_graph.addSeries(byh)
#         if myn !=  "None":
#            self.m_graph.addSeries(myn)
#         if shk !=  "None":
#            self.m_graph.addSeries(shk)
#         if khq !=  "None":
#            self.m_graph.addSeries(khq)
#         if ttf !=  "None":
#            self.m_graph.addSeries(ttf)
#         if scm !=  "None":
#            self.m_graph.addSeries(scm)
#         if qht !=  "None":
#            self.m_graph.addSeries(qht)
#         if xae !=  "None":
#            self.m_graph.addSeries(xae)
#         if mlb !=  "None":
#            self.m_graph.addSeries(mlb)
#         if xtq !=  "None":
#            self.m_graph.addSeries(xtq)
#         if cxq !=  "None":
#            self.m_graph.addSeries(cxq)
#         if agb !=  "None":
#            self.m_graph.addSeries(agb)
#         if hvo !=  "None":
#            self.m_graph.addSeries(hvo)
#         if iec !=  "None":
#            self.m_graph.addSeries(iec)
#         if xmy !=  "None":
#            self.m_graph.addSeries(xmy)
#         if qbl !=  "None":
#            self.m_graph.addSeries(qbl)
#         if xtg !=  "None":
#            self.m_graph.addSeries(xtg)
#         if kaz !=  "None":
#            self.m_graph.addSeries(kaz)
#         if bzx !=  "None":
#            self.m_graph.addSeries(bzx)
#         if zsl !=  "None":
#            self.m_graph.addSeries(zsl)
#         if gtn !=  "None":
#            self.m_graph.addSeries(gtn)
#         if afp !=  "None":
#            self.m_graph.addSeries(afp)
#         if hvd !=  "None":
#            self.m_graph.addSeries(hvd)
#         if uen !=  "None":
#            self.m_graph.addSeries(uen)
#         if ute !=  "None":
#            self.m_graph.addSeries(ute)
#         if njv !=  "None":
#            self.m_graph.addSeries(njv)
#         if lvx !=  "None":
#            self.m_graph.addSeries(lvx)
#         if zzj !=  "None":
#            self.m_graph.addSeries(zzj)
#         if exc !=  "None":
#            self.m_graph.addSeries(exc)
#         if krr !=  "None":
#            self.m_graph.addSeries(krr)
#         if hpd !=  "None":
#            self.m_graph.addSeries(hpd)
#         if tee !=  "None":
#            self.m_graph.addSeries(tee)
#         if utf !=  "None":
#            self.m_graph.addSeries(utf)
#         if rgz !=  "None":
#            self.m_graph.addSeries(rgz)
#         if ebc !=  "None":
#            self.m_graph.addSeries(ebc)
#         if rjh !=  "None":
#            self.m_graph.addSeries(rjh)
#         if rof !=  "None":
#            self.m_graph.addSeries(rof)
#         if lum !=  "None":
#            self.m_graph.addSeries(lum)
#         if uli !=  "None":
#            self.m_graph.addSeries(uli)
#         if huk !=  "None":
#            self.m_graph.addSeries(huk)
#         if rum !=  "None":
#            self.m_graph.addSeries(rum)
#         if sog !=  "None":
#            self.m_graph.addSeries(sog)
#         if mln !=  "None":
#            self.m_graph.addSeries(mln)
#         if uok !=  "None":
#            self.m_graph.addSeries(uok)
#         if mif !=  "None":
#            self.m_graph.addSeries(mif)
#         if hwb !=  "None":
#            self.m_graph.addSeries(hwb)
#         if lfn !=  "None":
#            self.m_graph.addSeries(lfn)
#         if imc !=  "None":
#            self.m_graph.addSeries(imc)
#         if vqj !=  "None":
#            self.m_graph.addSeries(vqj)
#         if mgm !=  "None":
#            self.m_graph.addSeries(mgm)
#         if hbi !=  "None":
#            self.m_graph.addSeries(hbi)
#         if pmb !=  "None":
#            self.m_graph.addSeries(pmb)
#         if aqr !=  "None":
#            self.m_graph.addSeries(aqr)
#         if myd !=  "None":
#            self.m_graph.addSeries(myd)
#         if dcm !=  "None":
#            self.m_graph.addSeries(dcm)
#         if xgj !=  "None":
#            self.m_graph.addSeries(xgj)
#         if hvz !=  "None":
#            self.m_graph.addSeries(hvz)
#         if tyi !=  "None":
#            self.m_graph.addSeries(tyi)
#         if yhp !=  "None":
#            self.m_graph.addSeries(yhp)
#         if pfl !=  "None":
#            self.m_graph.addSeries(pfl)
#         if qpt !=  "None":
#            self.m_graph.addSeries(qpt)
#         if lvv !=  "None":
#            self.m_graph.addSeries(lvv)
#         if hyj !=  "None":
#            self.m_graph.addSeries(hyj)
#         if vlf !=  "None":
#            self.m_graph.addSeries(vlf)
#         if uzy !=  "None":
#            self.m_graph.addSeries(uzy)
#         if son !=  "None":
#            self.m_graph.addSeries(son)
#         if nze !=  "None":
#            self.m_graph.addSeries(nze)
#         if tmn !=  "None":
#            self.m_graph.addSeries(tmn)
#         if zfw !=  "None":
#            self.m_graph.addSeries(zfw)
#         if sid !=  "None":
#            self.m_graph.addSeries(sid)
#         if yov !=  "None":
#            self.m_graph.addSeries(yov)
#         if unq !=  "None":
#            self.m_graph.addSeries(unq)
#         if fqq !=  "None":
#            self.m_graph.addSeries(fqq)
#         if woy !=  "None":
#            self.m_graph.addSeries(woy)
#         if fik !=  "None":
#            self.m_graph.addSeries(fik)
#         if xbw !=  "None":
#            self.m_graph.addSeries(xbw)
#         if fwa !=  "None":
#            self.m_graph.addSeries(fwa)
#         if rqs !=  "None":
#            self.m_graph.addSeries(rqs)
#         if ehd !=  "None":
#            self.m_graph.addSeries(ehd)
#         if rza !=  "None":
#            self.m_graph.addSeries(rza)
#         if ngj !=  "None":
#            self.m_graph.addSeries(ngj)
#         if pxi !=  "None":
#            self.m_graph.addSeries(pxi)
#         if moo !=  "None":
#            self.m_graph.addSeries(moo)
#         if jrt !=  "None":
#            self.m_graph.addSeries(jrt)
#         if hni !=  "None":
#            self.m_graph.addSeries(hni)
#         if fth !=  "None":
#            self.m_graph.addSeries(fth)
#         if jyn !=  "None":
#            self.m_graph.addSeries(jyn)
#         if vef !=  "None":
#            self.m_graph.addSeries(vef)
#         if hak !=  "None":
#            self.m_graph.addSeries(hak)
#         if wlj !=  "None":
#            self.m_graph.addSeries(wlj)
#         if otv !=  "None":
#            self.m_graph.addSeries(otv)
#         if nwk !=  "None":
#            self.m_graph.addSeries(nwk)
#         if jfq !=  "None":
#            self.m_graph.addSeries(jfq)
#         if pbw !=  "None":
#            self.m_graph.addSeries(pbw)
#         if ffd !=  "None":
#            self.m_graph.addSeries(ffd)
#         if trl !=  "None":
#            self.m_graph.addSeries(trl)
#         if eje !=  "None":
#            self.m_graph.addSeries(eje)
#         if chj !=  "None":
#            self.m_graph.addSeries(chj)
#         if nen !=  "None":
#            self.m_graph.addSeries(nen)
#         if pjs !=  "None":
#            self.m_graph.addSeries(pjs)
#         if uds !=  "None":
#            self.m_graph.addSeries(uds)
#         if gaf !=  "None":
#            self.m_graph.addSeries(gaf)
#         if bsn !=  "None":
#            self.m_graph.addSeries(bsn)
#         if yhs !=  "None":
#            self.m_graph.addSeries(yhs)
#         if zvz !=  "None":
#            self.m_graph.addSeries(zvz)
#         if kqe !=  "None":
#            self.m_graph.addSeries(kqe)
#         if smb !=  "None":
#            self.m_graph.addSeries(smb)
#         if ulc !=  "None":
#            self.m_graph.addSeries(ulc)
#         if hrc !=  "None":
#            self.m_graph.addSeries(hrc)
#         if rdb !=  "None":
#            self.m_graph.addSeries(rdb)
#         if ytf !=  "None":
#            self.m_graph.addSeries(ytf)
#         if fwy !=  "None":
#            self.m_graph.addSeries(fwy)
#         if jvu !=  "None":
#            self.m_graph.addSeries(jvu)
#         if tfy !=  "None":
#            self.m_graph.addSeries(tfy)
#         if sci !=  "None":
#            self.m_graph.addSeries(sci)
#         if oxq !=  "None":
#            self.m_graph.addSeries(oxq)
#         if edj !=  "None":
#            self.m_graph.addSeries(edj)
#         if eyd !=  "None":
#            self.m_graph.addSeries(eyd)
#         if wik !=  "None":
#            self.m_graph.addSeries(wik)
#         if avc !=  "None":
#            self.m_graph.addSeries(avc)
#         if che !=  "None":
#            self.m_graph.addSeries(che)
#         if qin !=  "None":
#            self.m_graph.addSeries(qin)
#         if iwu !=  "None":
#            self.m_graph.addSeries(iwu)
#         if adb !=  "None":
#            self.m_graph.addSeries(adb)
#         if ymt !=  "None":
#            self.m_graph.addSeries(ymt)
#         if hxl !=  "None":
#            self.m_graph.addSeries(hxl)
#         if yot !=  "None":
#            self.m_graph.addSeries(yot)
#         if dud !=  "None":
#            self.m_graph.addSeries(dud)
#         if omv !=  "None":
#            self.m_graph.addSeries(omv)
#         if jus !=  "None":
#            self.m_graph.addSeries(jus)
#         if qau !=  "None":
#            self.m_graph.addSeries(qau)
#         if qwi !=  "None":
#            self.m_graph.addSeries(qwi)
#         if etw !=  "None":
#            self.m_graph.addSeries(etw)
#         if con !=  "None":
#            self.m_graph.addSeries(con)
#         if kzn !=  "None":
#            self.m_graph.addSeries(kzn)
#         if bxc !=  "None":
#            self.m_graph.addSeries(bxc)
#         if kid !=  "None":
#            self.m_graph.addSeries(kid)
#         if far !=  "None":
#            self.m_graph.addSeries(far)
#         if wpl !=  "None":
#            self.m_graph.addSeries(wpl)
#         if pgl !=  "None":
#            self.m_graph.addSeries(pgl)
#         if oaz !=  "None":
#            self.m_graph.addSeries(oaz)
#         if fgj !=  "None":
#            self.m_graph.addSeries(fgj)
#         if lqk !=  "None":
#            self.m_graph.addSeries(lqk)
#         if dct !=  "None":
#            self.m_graph.addSeries(dct)
#         if brl !=  "None":
#            self.m_graph.addSeries(brl)
#         if yxr !=  "None":
#            self.m_graph.addSeries(yxr)
#         if tcj !=  "None":
#            self.m_graph.addSeries(tcj)
#         if wrc !=  "None":
#            self.m_graph.addSeries(wrc)
#         if tof !=  "None":
#            self.m_graph.addSeries(tof)
#         if lbz !=  "None":
#            self.m_graph.addSeries(lbz)
#         if sha !=  "None":
#            self.m_graph.addSeries(sha)
#         if ghv !=  "None":
#            self.m_graph.addSeries(ghv)
#         if ljk !=  "None":
#            self.m_graph.addSeries(ljk)
#         if jxs !=  "None":
#            self.m_graph.addSeries(jxs)
#         if xfh !=  "None":
#            self.m_graph.addSeries(xfh)
#         if vrd !=  "None":
#            self.m_graph.addSeries(vrd)
#         if vej !=  "None":
#            self.m_graph.addSeries(vej)
#         if nkm !=  "None":
#            self.m_graph.addSeries(nkm)
#         if jnr !=  "None":
#            self.m_graph.addSeries(jnr)
#         if qwj !=  "None":
#            self.m_graph.addSeries(qwj)
#         if dbp !=  "None":
#            self.m_graph.addSeries(dbp)
#         if orl !=  "None":
#            self.m_graph.addSeries(orl)
#         if ypw !=  "None":
#            self.m_graph.addSeries(ypw)
#         if xxd !=  "None":
#            self.m_graph.addSeries(xxd)
#         if agt !=  "None":
#            self.m_graph.addSeries(agt)
#         if sdr !=  "None":
#            self.m_graph.addSeries(sdr)
#         if oen !=  "None":
#            self.m_graph.addSeries(oen)
#         if snx !=  "None":
#            self.m_graph.addSeries(snx)
#         if mpp !=  "None":
#            self.m_graph.addSeries(mpp)
#         if ath !=  "None":
#            self.m_graph.addSeries(ath)
#         if hyi !=  "None":
#            self.m_graph.addSeries(hyi)
#         if znb !=  "None":
#            self.m_graph.addSeries(znb)
#         if otb !=  "None":
#            self.m_graph.addSeries(otb)
#         if nfu !=  "None":
#            self.m_graph.addSeries(nfu)
#         if nyt !=  "None":
#            self.m_graph.addSeries(nyt)
#         if aen !=  "None":
#            self.m_graph.addSeries(aen)
#         if tme !=  "None":
#            self.m_graph.addSeries(tme)
#         if icb !=  "None":
#            self.m_graph.addSeries(icb)
#         if gck !=  "None":
#            self.m_graph.addSeries(gck)
#         if vpk !=  "None":
#            self.m_graph.addSeries(vpk)
#         if yub !=  "None":
#            self.m_graph.addSeries(yub)
#         if vio !=  "None":
#            self.m_graph.addSeries(vio)
#         if zfk !=  "None":
#            self.m_graph.addSeries(zfk)
#         if dte !=  "None":
#            self.m_graph.addSeries(dte)
#         if mrs !=  "None":
#            self.m_graph.addSeries(mrs)
#         if xxt !=  "None":
#            self.m_graph.addSeries(xxt)
#         if fxo !=  "None":
#            self.m_graph.addSeries(fxo)
#         if lrk !=  "None":
#            self.m_graph.addSeries(lrk)
#         if qri !=  "None":
#            self.m_graph.addSeries(qri)
#         if hoc !=  "None":
#            self.m_graph.addSeries(hoc)
#         if qvn !=  "None":
#            self.m_graph.addSeries(qvn)
#         if ibl !=  "None":
#            self.m_graph.addSeries(ibl)
#         if biu !=  "None":
#            self.m_graph.addSeries(biu)
#         if zym !=  "None":
#            self.m_graph.addSeries(zym)
#         if dyk !=  "None":
#            self.m_graph.addSeries(dyk)
#         if cmu !=  "None":
#            self.m_graph.addSeries(cmu)
#         if fix !=  "None":
#            self.m_graph.addSeries(fix)
#         if nvo !=  "None":
#            self.m_graph.addSeries(nvo)
#         if dlm !=  "None":
#            self.m_graph.addSeries(dlm)
#         if zzm !=  "None":
#            self.m_graph.addSeries(zzm)
#         if iko !=  "None":
#            self.m_graph.addSeries(iko)
#         if rmq !=  "None":
#            self.m_graph.addSeries(rmq)
#         if jmc !=  "None":
#            self.m_graph.addSeries(jmc)
#         if lsq !=  "None":
#            self.m_graph.addSeries(lsq)
#         if eyq !=  "None":
#            self.m_graph.addSeries(eyq)
#         if suf !=  "None":
#            self.m_graph.addSeries(suf)
#         if kqb !=  "None":
#            self.m_graph.addSeries(kqb)
#         if swg !=  "None":
#            self.m_graph.addSeries(swg)
#         if ium !=  "None":
#            self.m_graph.addSeries(ium)
#         if voq !=  "None":
#            self.m_graph.addSeries(voq)
#         if yzv !=  "None":
#            self.m_graph.addSeries(yzv)
#         if jbu !=  "None":
#            self.m_graph.addSeries(jbu)
#         if jcr !=  "None":
#            self.m_graph.addSeries(jcr)
#         if hym !=  "None":
#            self.m_graph.addSeries(hym)
#         if cmg !=  "None":
#            self.m_graph.addSeries(cmg)
#         if evz !=  "None":
#            self.m_graph.addSeries(evz)
#         if znn !=  "None":
#            self.m_graph.addSeries(znn)
#         if fre !=  "None":
#            self.m_graph.addSeries(fre)
#         if klv !=  "None":
#            self.m_graph.addSeries(klv)
#         if ian !=  "None":
#            self.m_graph.addSeries(ian)
#         if lsw !=  "None":
#            self.m_graph.addSeries(lsw)
#         if jod !=  "None":
#            self.m_graph.addSeries(jod)
#         if kxk !=  "None":
#            self.m_graph.addSeries(kxk)
#         if swi !=  "None":
#            self.m_graph.addSeries(swi)
#         if kgb !=  "None":
#            self.m_graph.addSeries(kgb)
#         if eis !=  "None":
#            self.m_graph.addSeries(eis)
#         if qnc !=  "None":
#            self.m_graph.addSeries(qnc)
#         if usy !=  "None":
#            self.m_graph.addSeries(usy)
#         if cmi !=  "None":
#            self.m_graph.addSeries(cmi)
#         if mjq !=  "None":
#            self.m_graph.addSeries(mjq)
#         if uie !=  "None":
#            self.m_graph.addSeries(uie)
#         if inp !=  "None":
#            self.m_graph.addSeries(inp)
#         if iuy !=  "None":
#            self.m_graph.addSeries(iuy)
#         if rnj !=  "None":
#            self.m_graph.addSeries(rnj)
#         if zzv !=  "None":
#            self.m_graph.addSeries(zzv)
#         if ulv !=  "None":
#            self.m_graph.addSeries(ulv)
#         if zqt !=  "None":
#            self.m_graph.addSeries(zqt)
#         if suo !=  "None":
#            self.m_graph.addSeries(suo)
#         if zeq !=  "None":
#            self.m_graph.addSeries(zeq)
#         if huv !=  "None":
#            self.m_graph.addSeries(huv)
#         if ldq !=  "None":
#            self.m_graph.addSeries(ldq)
#         if abm !=  "None":
#            self.m_graph.addSeries(abm)
#         if ojp !=  "None":
#            self.m_graph.addSeries(ojp)
#         if myb !=  "None":
#            self.m_graph.addSeries(myb)
#         if uyj !=  "None":
#            self.m_graph.addSeries(uyj)
#         if sbv !=  "None":
#            self.m_graph.addSeries(sbv)
#         if yif !=  "None":
#            self.m_graph.addSeries(yif)
#         if fvi !=  "None":
#            self.m_graph.addSeries(fvi)
#         if rer !=  "None":
#            self.m_graph.addSeries(rer)
#         if mem !=  "None":
#            self.m_graph.addSeries(mem)
#         if dig !=  "None":
#            self.m_graph.addSeries(dig)
#         if zew !=  "None":
#            self.m_graph.addSeries(zew)
#         if sgk !=  "None":
#            self.m_graph.addSeries(sgk)
#         if erv !=  "None":
#            self.m_graph.addSeries(erv)
#         if bxu !=  "None":
#            self.m_graph.addSeries(bxu)
#         if pns !=  "None":
#            self.m_graph.addSeries(pns)
#         if ioo !=  "None":
#            self.m_graph.addSeries(ioo)
#         if jdo !=  "None":
#            self.m_graph.addSeries(jdo)
#         if aev !=  "None":
#            self.m_graph.addSeries(aev)
#         if fxh !=  "None":
#            self.m_graph.addSeries(fxh)
#         if wxv !=  "None":
#            self.m_graph.addSeries(wxv)
#         if cnd !=  "None":
#            self.m_graph.addSeries(cnd)
#         if upg !=  "None":
#            self.m_graph.addSeries(upg)
#         if vux !=  "None":
#            self.m_graph.addSeries(vux)
#         if ken !=  "None":
#            self.m_graph.addSeries(ken)
#         if wkw !=  "None":
#            self.m_graph.addSeries(wkw)
#         if ivm !=  "None":
#            self.m_graph.addSeries(ivm)
#         if oqm !=  "None":
#            self.m_graph.addSeries(oqm)
#         if qvx !=  "None":
#            self.m_graph.addSeries(qvx)
#         if ncx !=  "None":
#            self.m_graph.addSeries(ncx)
#         if pax !=  "None":
#            self.m_graph.addSeries(pax)
#         if gkx !=  "None":
#            self.m_graph.addSeries(gkx)
#         if vrh !=  "None":
#            self.m_graph.addSeries(vrh)
#         if vsi !=  "None":
#            self.m_graph.addSeries(vsi)
#         if wnn !=  "None":
#            self.m_graph.addSeries(wnn)
#         if irs !=  "None":
#            self.m_graph.addSeries(irs)
#         if igd !=  "None":
#            self.m_graph.addSeries(igd)
#         if gwf !=  "None":
#            self.m_graph.addSeries(gwf)
#         if ldo !=  "None":
#            self.m_graph.addSeries(ldo)
#         if rfx !=  "None":
#            self.m_graph.addSeries(rfx)
#         if unv !=  "None":
#            self.m_graph.addSeries(unv)
#         if heg !=  "None":
#            self.m_graph.addSeries(heg)
#         if xtk !=  "None":
#            self.m_graph.addSeries(xtk)
#         if axk !=  "None":
#            self.m_graph.addSeries(axk)
#         if rbz !=  "None":
#            self.m_graph.addSeries(rbz)
#         if gjd !=  "None":
#            self.m_graph.addSeries(gjd)
#         if xfj !=  "None":
#            self.m_graph.addSeries(xfj)
#         if opk !=  "None":
#            self.m_graph.addSeries(opk)
#         if pwp !=  "None":
#            self.m_graph.addSeries(pwp)
#         if czh !=  "None":
#            self.m_graph.addSeries(czh)
#         if nhq !=  "None":
#            self.m_graph.addSeries(nhq)
#         if wxf !=  "None":
#            self.m_graph.addSeries(wxf)
#         if wrw !=  "None":
#            self.m_graph.addSeries(wrw)
#         if nnz !=  "None":
#            self.m_graph.addSeries(nnz)
#         if riw !=  "None":
#            self.m_graph.addSeries(riw)
#         if aui !=  "None":
#            self.m_graph.addSeries(aui)
#         if lgx !=  "None":
#            self.m_graph.addSeries(lgx)
#         if tue !=  "None":
#            self.m_graph.addSeries(tue)
#         if yly !=  "None":
#            self.m_graph.addSeries(yly)
#         if uwj !=  "None":
#            self.m_graph.addSeries(uwj)
#         if cbv !=  "None":
#            self.m_graph.addSeries(cbv)
#         if aea !=  "None":
#            self.m_graph.addSeries(aea)
#         if fav !=  "None":
#            self.m_graph.addSeries(fav)
#         if hku !=  "None":
#            self.m_graph.addSeries(hku)
#         if pvc !=  "None":
#            self.m_graph.addSeries(pvc)
#         if wei !=  "None":
#            self.m_graph.addSeries(wei)
#         if gkz !=  "None":
#            self.m_graph.addSeries(gkz)
#         if pgv !=  "None":
#            self.m_graph.addSeries(pgv)
#         if yuc !=  "None":
#            self.m_graph.addSeries(yuc)
#         if iwh !=  "None":
#            self.m_graph.addSeries(iwh)
#         if xqo !=  "None":
#            self.m_graph.addSeries(xqo)
#         if ota !=  "None":
#            self.m_graph.addSeries(ota)
#         if qew !=  "None":
#            self.m_graph.addSeries(qew)
#         if dqg !=  "None":
#            self.m_graph.addSeries(dqg)
#         if bfg !=  "None":
#            self.m_graph.addSeries(bfg)
#         if ynz !=  "None":
#            self.m_graph.addSeries(ynz)
#         if exw !=  "None":
#            self.m_graph.addSeries(exw)
#         if sud !=  "None":
#            self.m_graph.addSeries(sud)
#         if vhj !=  "None":
#            self.m_graph.addSeries(vhj)
#         if ges !=  "None":
#            self.m_graph.addSeries(ges)
#         if amw !=  "None":
#            self.m_graph.addSeries(amw)
#         if iqt !=  "None":
#            self.m_graph.addSeries(iqt)
#         if kol !=  "None":
#            self.m_graph.addSeries(kol)
#         if hfa !=  "None":
#            self.m_graph.addSeries(hfa)
#         if fvu !=  "None":
#            self.m_graph.addSeries(fvu)
#         if qsi !=  "None":
#            self.m_graph.addSeries(qsi)
#         if qix !=  "None":
#            self.m_graph.addSeries(qix)
#         if tcr !=  "None":
#            self.m_graph.addSeries(tcr)
#         if ctk !=  "None":
#            self.m_graph.addSeries(ctk)
#         if qqg !=  "None":
#            self.m_graph.addSeries(qqg)
#         if wze !=  "None":
#            self.m_graph.addSeries(wze)
#         if hod !=  "None":
#            self.m_graph.addSeries(hod)
#         if hzr !=  "None":
#            self.m_graph.addSeries(hzr)
#         if nlh !=  "None":
#            self.m_graph.addSeries(nlh)
#         if qso !=  "None":
#            self.m_graph.addSeries(qso)
#         if pja !=  "None":
#            self.m_graph.addSeries(pja)
#         if oqe !=  "None":
#            self.m_graph.addSeries(oqe)
#         if rst !=  "None":
#            self.m_graph.addSeries(rst)
#         if fzh !=  "None":
#            self.m_graph.addSeries(fzh)
#         if awz !=  "None":
#            self.m_graph.addSeries(awz)
#         if atn !=  "None":
#            self.m_graph.addSeries(atn)
#         if fwb !=  "None":
#            self.m_graph.addSeries(fwb)
#         if txd !=  "None":
#            self.m_graph.addSeries(txd)
#         if ybg !=  "None":
#            self.m_graph.addSeries(ybg)
#         if tpe !=  "None":
#            self.m_graph.addSeries(tpe)
#         if how !=  "None":
#            self.m_graph.addSeries(how)
#         if nuu !=  "None":
#            self.m_graph.addSeries(nuu)
#         if wam !=  "None":
#            self.m_graph.addSeries(wam)
#         if oiw !=  "None":
#            self.m_graph.addSeries(oiw)
#         if mrc !=  "None":
#            self.m_graph.addSeries(mrc)
#         if wjo !=  "None":
#            self.m_graph.addSeries(wjo)
#         if yfw !=  "None":
#            self.m_graph.addSeries(yfw)
#         if nxm !=  "None":
#            self.m_graph.addSeries(nxm)
#         if rqn !=  "None":
#            self.m_graph.addSeries(rqn)
#         if aju !=  "None":
#            self.m_graph.addSeries(aju)
#         if eyh !=  "None":
#            self.m_graph.addSeries(eyh)
#         if xsj !=  "None":
#            self.m_graph.addSeries(xsj)
#         if zyp !=  "None":
#            self.m_graph.addSeries(zyp)
#         if hee !=  "None":
#            self.m_graph.addSeries(hee)
#         if coj !=  "None":
#            self.m_graph.addSeries(coj)
#         if xzj !=  "None":
#            self.m_graph.addSeries(xzj)
#         if uzf !=  "None":
#            self.m_graph.addSeries(uzf)
#         if sbb !=  "None":
#            self.m_graph.addSeries(sbb)
#         if wah !=  "None":
#            self.m_graph.addSeries(wah)
#         if ldz !=  "None":
#            self.m_graph.addSeries(ldz)
#         if emu !=  "None":
#            self.m_graph.addSeries(emu)
#         if umg !=  "None":
#            self.m_graph.addSeries(umg)
#         if fpi !=  "None":
#            self.m_graph.addSeries(fpi)
#         if zpz !=  "None":
#            self.m_graph.addSeries(zpz)
#         if mzh !=  "None":
#            self.m_graph.addSeries(mzh)
#         if hqu !=  "None":
#            self.m_graph.addSeries(hqu)
#         if eoz !=  "None":
#            self.m_graph.addSeries(eoz)
#         if zxg !=  "None":
#            self.m_graph.addSeries(zxg)
#         if ncc !=  "None":
#            self.m_graph.addSeries(ncc)
#         if kbs !=  "None":
#            self.m_graph.addSeries(kbs)
#         if usi !=  "None":
#            self.m_graph.addSeries(usi)
#         if hzi !=  "None":
#            self.m_graph.addSeries(hzi)
#         if rbh !=  "None":
#            self.m_graph.addSeries(rbh)
#         if kun !=  "None":
#            self.m_graph.addSeries(kun)
#         if aoi !=  "None":
#            self.m_graph.addSeries(aoi)
#         if qwm !=  "None":
#            self.m_graph.addSeries(qwm)
#         if uyc !=  "None":
#            self.m_graph.addSeries(uyc)
#         if duh !=  "None":
#            self.m_graph.addSeries(duh)
#         if eyn !=  "None":
#            self.m_graph.addSeries(eyn)
#         if gdh !=  "None":
#            self.m_graph.addSeries(gdh)
#         if lca !=  "None":
#            self.m_graph.addSeries(lca)
#         if ubu !=  "None":
#            self.m_graph.addSeries(ubu)
#         if zsz !=  "None":
#            self.m_graph.addSeries(zsz)
#         if dns !=  "None":
#            self.m_graph.addSeries(dns)
#         if xxn !=  "None":
#            self.m_graph.addSeries(xxn)
#         if zyg !=  "None":
#            self.m_graph.addSeries(zyg)
#         if cec !=  "None":
#            self.m_graph.addSeries(cec)
#         if bla !=  "None":
#            self.m_graph.addSeries(bla)
#         if unp !=  "None":
#            self.m_graph.addSeries(unp)
#         if rjg !=  "None":
#            self.m_graph.addSeries(rjg)
#         if gti !=  "None":
#            self.m_graph.addSeries(gti)
#         if qfc !=  "None":
#            self.m_graph.addSeries(qfc)
#         if nrj !=  "None":
#            self.m_graph.addSeries(nrj)
#         if hxf !=  "None":
#            self.m_graph.addSeries(hxf)
#         if ayh !=  "None":
#            self.m_graph.addSeries(ayh)
#         if hkg !=  "None":
#            self.m_graph.addSeries(hkg)
#         if akd !=  "None":
#            self.m_graph.addSeries(akd)
#         if nfw !=  "None":
#            self.m_graph.addSeries(nfw)
#         if ouc !=  "None":
#            self.m_graph.addSeries(ouc)
#         if sul !=  "None":
#            self.m_graph.addSeries(sul)
#         if isf !=  "None":
#            self.m_graph.addSeries(isf)
#         if biq !=  "None":
#            self.m_graph.addSeries(biq)
#         if zun !=  "None":
#            self.m_graph.addSeries(zun)
#         if khc !=  "None":
#            self.m_graph.addSeries(khc)
#         if xpj !=  "None":
#            self.m_graph.addSeries(xpj)
#         if grn !=  "None":
#            self.m_graph.addSeries(grn)
#         if hut !=  "None":
#            self.m_graph.addSeries(hut)
#         if bzo !=  "None":
#            self.m_graph.addSeries(bzo)
#         if zzl !=  "None":
#            self.m_graph.addSeries(zzl)
#         if wpu !=  "None":
#            self.m_graph.addSeries(wpu)
#         if ihi !=  "None":
#            self.m_graph.addSeries(ihi)
#         if syo !=  "None":
#            self.m_graph.addSeries(syo)
#         if rsw !=  "None":
#            self.m_graph.addSeries(rsw)
#         if ivn !=  "None":
#            self.m_graph.addSeries(ivn)
#         if jcy !=  "None":
#            self.m_graph.addSeries(jcy)
#         if ivi !=  "None":
#            self.m_graph.addSeries(ivi)
#         if biy !=  "None":
#            self.m_graph.addSeries(biy)
#         if jhc !=  "None":
#            self.m_graph.addSeries(jhc)
#         if izz !=  "None":
#            self.m_graph.addSeries(izz)
#         if vlx !=  "None":
#            self.m_graph.addSeries(vlx)
#         if lyr !=  "None":
#            self.m_graph.addSeries(lyr)
#         if kmy !=  "None":
#            self.m_graph.addSeries(kmy)
#         if dsl !=  "None":
#            self.m_graph.addSeries(dsl)
#         if ptb !=  "None":
#            self.m_graph.addSeries(ptb)
#         if evn !=  "None":
#            self.m_graph.addSeries(evn)
#         if ciw !=  "None":
#            self.m_graph.addSeries(ciw)
#         if kht !=  "None":
#            self.m_graph.addSeries(kht)
#         if lmb !=  "None":
#            self.m_graph.addSeries(lmb)
#         if rpp !=  "None":
#            self.m_graph.addSeries(rpp)
#         if uln !=  "None":
#            self.m_graph.addSeries(uln)
#         if yha !=  "None":
#            self.m_graph.addSeries(yha)
#         if dhq !=  "None":
#            self.m_graph.addSeries(dhq)
#         if tkk !=  "None":
#            self.m_graph.addSeries(tkk)
#         if ayp !=  "None":
#            self.m_graph.addSeries(ayp)
#         if ija !=  "None":
#            self.m_graph.addSeries(ija)
#         if rnd !=  "None":
#            self.m_graph.addSeries(rnd)
#         if ztc !=  "None":
#            self.m_graph.addSeries(ztc)
#         if fxl !=  "None":
#            self.m_graph.addSeries(fxl)
#         if sly !=  "None":
#            self.m_graph.addSeries(sly)
#         if rig !=  "None":
#            self.m_graph.addSeries(rig)
#         if xdh !=  "None":
#            self.m_graph.addSeries(xdh)
#         if xnz !=  "None":
#            self.m_graph.addSeries(xnz)
#         if ufa !=  "None":
#            self.m_graph.addSeries(ufa)
#         if ehv !=  "None":
#            self.m_graph.addSeries(ehv)
#         if zkv !=  "None":
#            self.m_graph.addSeries(zkv)
#         if jpm !=  "None":
#            self.m_graph.addSeries(jpm)
#         if jyb !=  "None":
#            self.m_graph.addSeries(jyb)
#         if jyu !=  "None":
#            self.m_graph.addSeries(jyu)
#         if ukn !=  "None":
#            self.m_graph.addSeries(ukn)
#         if qeh !=  "None":
#            self.m_graph.addSeries(qeh)
#         if yal !=  "None":
#            self.m_graph.addSeries(yal)
#         if mlg !=  "None":
#            self.m_graph.addSeries(mlg)
#         if yup !=  "None":
#            self.m_graph.addSeries(yup)
#         if puk !=  "None":
#            self.m_graph.addSeries(puk)
#         if cof !=  "None":
#            self.m_graph.addSeries(cof)
#         if bvl !=  "None":
#            self.m_graph.addSeries(bvl)
#         if gjv !=  "None":
#            self.m_graph.addSeries(gjv)
#         if stg !=  "None":
#            self.m_graph.addSeries(stg)
#         if gjk !=  "None":
#            self.m_graph.addSeries(gjk)
#         if ofr !=  "None":
#            self.m_graph.addSeries(ofr)
#         if utn !=  "None":
#            self.m_graph.addSeries(utn)
#         if sis !=  "None":
#            self.m_graph.addSeries(sis)
#         if yjo !=  "None":
#            self.m_graph.addSeries(yjo)
#         if ewj !=  "None":
#            self.m_graph.addSeries(ewj)
#         if pdb !=  "None":
#            self.m_graph.addSeries(pdb)
#         if lac !=  "None":
#            self.m_graph.addSeries(lac)
#         if ajp !=  "None":
#            self.m_graph.addSeries(ajp)
#         if esr !=  "None":
#            self.m_graph.addSeries(esr)
#         if ovc !=  "None":
#            self.m_graph.addSeries(ovc)
#         if bcv !=  "None":
#            self.m_graph.addSeries(bcv)
#         if nqx !=  "None":
#            self.m_graph.addSeries(nqx)
#         if znq !=  "None":
#            self.m_graph.addSeries(znq)
#         if utk !=  "None":
#            self.m_graph.addSeries(utk)
#         if jmz !=  "None":
#            self.m_graph.addSeries(jmz)
#         if xwg !=  "None":
#            self.m_graph.addSeries(xwg)
#         if yfp !=  "None":
#            self.m_graph.addSeries(yfp)
#         if wkn !=  "None":
#            self.m_graph.addSeries(wkn)
#         if prm !=  "None":
#            self.m_graph.addSeries(prm)
#         if elr !=  "None":
#            self.m_graph.addSeries(elr)
#         if ile !=  "None":
#            self.m_graph.addSeries(ile)
#         if xpy !=  "None":
#            self.m_graph.addSeries(xpy)
#         if tss !=  "None":
#            self.m_graph.addSeries(tss)
#         if gei !=  "None":
#            self.m_graph.addSeries(gei)
#         if jfy !=  "None":
#            self.m_graph.addSeries(jfy)
#         if qzl !=  "None":
#            self.m_graph.addSeries(qzl)
#         if siv !=  "None":
#            self.m_graph.addSeries(siv)
#         if kyb !=  "None":
#            self.m_graph.addSeries(kyb)
#         if gil !=  "None":
#            self.m_graph.addSeries(gil)
#         if kqv !=  "None":
#            self.m_graph.addSeries(kqv)
#         if gjq !=  "None":
#            self.m_graph.addSeries(gjq)
#         if vbj !=  "None":
#            self.m_graph.addSeries(vbj)
#         if gtl !=  "None":
#            self.m_graph.addSeries(gtl)
#         if cbk !=  "None":
#            self.m_graph.addSeries(cbk)
#         if ehw !=  "None":
#            self.m_graph.addSeries(ehw)
#         if eyf !=  "None":
#            self.m_graph.addSeries(eyf)
#         if fce !=  "None":
#            self.m_graph.addSeries(fce)
#         if xsu !=  "None":
#            self.m_graph.addSeries(xsu)
#         if wzs !=  "None":
#            self.m_graph.addSeries(wzs)
#         if wbn !=  "None":
#            self.m_graph.addSeries(wbn)
#         if awa !=  "None":
#            self.m_graph.addSeries(awa)
#         if tze !=  "None":
#            self.m_graph.addSeries(tze)
#         if zvc !=  "None":
#            self.m_graph.addSeries(zvc)
#         if fnc !=  "None":
#            self.m_graph.addSeries(fnc)
#         if rda !=  "None":
#            self.m_graph.addSeries(rda)
#         if tqe !=  "None":
#            self.m_graph.addSeries(tqe)
#         if hft !=  "None":
#            self.m_graph.addSeries(hft)
#         if ctt !=  "None":
#            self.m_graph.addSeries(ctt)
#         if ufz !=  "None":
#            self.m_graph.addSeries(ufz)
#         if hjd !=  "None":
#            self.m_graph.addSeries(hjd)
#         if gsn !=  "None":
#            self.m_graph.addSeries(gsn)
#         if sgd !=  "None":
#            self.m_graph.addSeries(sgd)
#         if dji !=  "None":
#            self.m_graph.addSeries(dji)
#         if wmx !=  "None":
#            self.m_graph.addSeries(wmx)
#         if qds !=  "None":
#            self.m_graph.addSeries(qds)
#         if oiv !=  "None":
#            self.m_graph.addSeries(oiv)
#         if row !=  "None":
#            self.m_graph.addSeries(row)
#         if mhr !=  "None":
#            self.m_graph.addSeries(mhr)
#         if jql !=  "None":
#            self.m_graph.addSeries(jql)
#         if noe !=  "None":
#            self.m_graph.addSeries(noe)
#         if ohk !=  "None":
#            self.m_graph.addSeries(ohk)
#         if mdd !=  "None":
#            self.m_graph.addSeries(mdd)
#         if ocr !=  "None":
#            self.m_graph.addSeries(ocr)
#         if ltf !=  "None":
#            self.m_graph.addSeries(ltf)
#         if qrm !=  "None":
#            self.m_graph.addSeries(qrm)
#         if hou !=  "None":
#            self.m_graph.addSeries(hou)
#         if tli !=  "None":
#            self.m_graph.addSeries(tli)
#         if kuh !=  "None":
#            self.m_graph.addSeries(kuh)
#         if bnn !=  "None":
#            self.m_graph.addSeries(bnn)
#         if qzm !=  "None":
#            self.m_graph.addSeries(qzm)
#         if nvz !=  "None":
#            self.m_graph.addSeries(nvz)
#         if nug !=  "None":
#            self.m_graph.addSeries(nug)
#         if klc !=  "None":
#            self.m_graph.addSeries(klc)
#         if hwq !=  "None":
#            self.m_graph.addSeries(hwq)
#         if xmt !=  "None":
#            self.m_graph.addSeries(xmt)
#         if ozi !=  "None":
#            self.m_graph.addSeries(ozi)
#         if fog !=  "None":
#            self.m_graph.addSeries(fog)
#         if dcq !=  "None":
#            self.m_graph.addSeries(dcq)
#         if abq !=  "None":
#            self.m_graph.addSeries(abq)
#         if dio !=  "None":
#            self.m_graph.addSeries(dio)
#         if pxv !=  "None":
#            self.m_graph.addSeries(pxv)
#         if ani !=  "None":
#            self.m_graph.addSeries(ani)
#         if qwr !=  "None":
#            self.m_graph.addSeries(qwr)
#         if uyu !=  "None":
#            self.m_graph.addSeries(uyu)
#         if alv !=  "None":
#            self.m_graph.addSeries(alv)
#         if sce !=  "None":
#            self.m_graph.addSeries(sce)
#         if onu !=  "None":
#            self.m_graph.addSeries(onu)
#         if zkd !=  "None":
#            self.m_graph.addSeries(zkd)
#         if hfc !=  "None":
#            self.m_graph.addSeries(hfc)
#         if mcc !=  "None":
#            self.m_graph.addSeries(mcc)
#         if dne !=  "None":
#            self.m_graph.addSeries(dne)
#         if oak !=  "None":
#            self.m_graph.addSeries(oak)
#         if uuz !=  "None":
#            self.m_graph.addSeries(uuz)
#         if deb !=  "None":
#            self.m_graph.addSeries(deb)
#         if rod !=  "None":
#            self.m_graph.addSeries(rod)
#         if mzf !=  "None":
#            self.m_graph.addSeries(mzf)
#         if jzb !=  "None":
#            self.m_graph.addSeries(jzb)
#         if zvh !=  "None":
#            self.m_graph.addSeries(zvh)
#         if nzu !=  "None":
#            self.m_graph.addSeries(nzu)
#         if nzs !=  "None":
#            self.m_graph.addSeries(nzs)
#         if aza !=  "None":
#            self.m_graph.addSeries(aza)
#         if gch !=  "None":
#            self.m_graph.addSeries(gch)
#         if zuh !=  "None":
#            self.m_graph.addSeries(zuh)
#         if whs !=  "None":
#            self.m_graph.addSeries(whs)
#         if ugu !=  "None":
#            self.m_graph.addSeries(ugu)
#         if kuv !=  "None":
#            self.m_graph.addSeries(kuv)
#         if lqv !=  "None":
#            self.m_graph.addSeries(lqv)
#         if let !=  "None":
#            self.m_graph.addSeries(let)
#         if hvw !=  "None":
#            self.m_graph.addSeries(hvw)
#         if bov !=  "None":
#            self.m_graph.addSeries(bov)
#         if yna !=  "None":
#            self.m_graph.addSeries(yna)
#         if xzn !=  "None":
#            self.m_graph.addSeries(xzn)
#         if pvm !=  "None":
#            self.m_graph.addSeries(pvm)
#         if jdv !=  "None":
#            self.m_graph.addSeries(jdv)
#         if sls !=  "None":
#            self.m_graph.addSeries(sls)
#         if sbr !=  "None":
#            self.m_graph.addSeries(sbr)
#         if nnd !=  "None":
#            self.m_graph.addSeries(nnd)
#         if vtb !=  "None":
#            self.m_graph.addSeries(vtb)
#         if fbk !=  "None":
#            self.m_graph.addSeries(fbk)
#         if csj !=  "None":
#            self.m_graph.addSeries(csj)
#         if hqc !=  "None":
#            self.m_graph.addSeries(hqc)
#         if mrg !=  "None":
#            self.m_graph.addSeries(mrg)
#         if ozk !=  "None":
#            self.m_graph.addSeries(ozk)
#         if ctx !=  "None":
#            self.m_graph.addSeries(ctx)
#         if nvj !=  "None":
#            self.m_graph.addSeries(nvj)
#         if lrj !=  "None":
#            self.m_graph.addSeries(lrj)
#         if edx !=  "None":
#            self.m_graph.addSeries(edx)
#         if lyd !=  "None":
#            self.m_graph.addSeries(lyd)
#         if bqe !=  "None":
#            self.m_graph.addSeries(bqe)
#         if laj !=  "None":
#            self.m_graph.addSeries(laj)
#         if qlo !=  "None":
#            self.m_graph.addSeries(qlo)
#         if xfd !=  "None":
#            self.m_graph.addSeries(xfd)
#         if mkb !=  "None":
#            self.m_graph.addSeries(mkb)
#         if buw !=  "None":
#            self.m_graph.addSeries(buw)
#         if bgd !=  "None":
#            self.m_graph.addSeries(bgd)
#         if lmc !=  "None":
#            self.m_graph.addSeries(lmc)
#         if gll !=  "None":
#            self.m_graph.addSeries(gll)
#         if ywr !=  "None":
#            self.m_graph.addSeries(ywr)
#         if uei !=  "None":
#            self.m_graph.addSeries(uei)
#         if bvk !=  "None":
#            self.m_graph.addSeries(bvk)
#         if iyb !=  "None":
#            self.m_graph.addSeries(iyb)
#         if urk !=  "None":
#            self.m_graph.addSeries(urk)
#         if pmh !=  "None":
#            self.m_graph.addSeries(pmh)
#         if nzw !=  "None":
#            self.m_graph.addSeries(nzw)
#         if bmz !=  "None":
#            self.m_graph.addSeries(bmz)
#         if cmf !=  "None":
#            self.m_graph.addSeries(cmf)
#         if hzl !=  "None":
#            self.m_graph.addSeries(hzl)
#         if dr !=  "None":
#            self.m_graph.addSeries(dr)
#         if tvq !=  "None":
#            self.m_graph.addSeries(tvq)
#         if csd !=  "None":
#            self.m_graph.addSeries(csd)
#         if xns !=  "None":
#            self.m_graph.addSeries(xns)
#         if inq !=  "None":
#            self.m_graph.addSeries(inq)
#         if xzc !=  "None":
#            self.m_graph.addSeries(xzc)
#         if nmo !=  "None":
#            self.m_graph.addSeries(nmo)
#         if pql !=  "None":
#            self.m_graph.addSeries(pql)
#         if ufl !=  "None":
#            self.m_graph.addSeries(ufl)
#         if nja !=  "None":
#            self.m_graph.addSeries(nja)
#         if bya !=  "None":
#            self.m_graph.addSeries(bya)
#         if cuj !=  "None":
#            self.m_graph.addSeries(cuj)
#         if ikp !=  "None":
#            self.m_graph.addSeries(ikp)
#         if zzh !=  "None":
#            self.m_graph.addSeries(zzh)
#         if tbc !=  "None":
#            self.m_graph.addSeries(tbc)
#         if jqz !=  "None":
#            self.m_graph.addSeries(jqz)
#         if hlu !=  "None":
#            self.m_graph.addSeries(hlu)
#         if mhc !=  "None":
#            self.m_graph.addSeries(mhc)
#         if bgv !=  "None":
#            self.m_graph.addSeries(bgv)
#         if xcc !=  "None":
#            self.m_graph.addSeries(xcc)
#         if sft !=  "None":
#            self.m_graph.addSeries(sft)
#         if hlm !=  "None":
#            self.m_graph.addSeries(hlm)
#         if gxj !=  "None":
#            self.m_graph.addSeries(gxj)
#         if sqx !=  "None":
#            self.m_graph.addSeries(sqx)
#         if veq !=  "None":
#            self.m_graph.addSeries(veq)
#         if bos !=  "None":
#            self.m_graph.addSeries(bos)
#         if ddq !=  "None":
#            self.m_graph.addSeries(ddq)
#         if cuu !=  "None":
#            self.m_graph.addSeries(cuu)
#         if jbg !=  "None":
#            self.m_graph.addSeries(jbg)
#         if fkl !=  "None":
#            self.m_graph.addSeries(fkl)
#         if jhh !=  "None":
#            self.m_graph.addSeries(jhh)
#         if dov !=  "None":
#            self.m_graph.addSeries(dov)
#         if koq !=  "None":
#            self.m_graph.addSeries(koq)
#         if yze !=  "None":
#            self.m_graph.addSeries(yze)
#         if xmi !=  "None":
#            self.m_graph.addSeries(xmi)
#         if cuf !=  "None":
#            self.m_graph.addSeries(cuf)
#         if yfy !=  "None":
#            self.m_graph.addSeries(yfy)
#         if lwb !=  "None":
#            self.m_graph.addSeries(lwb)
#         if pte !=  "None":
#            self.m_graph.addSeries(pte)
#         if rks !=  "None":
#            self.m_graph.addSeries(rks)
#         if omz !=  "None":
#            self.m_graph.addSeries(omz)
#         if rws !=  "None":
#            self.m_graph.addSeries(rws)
#         if bjg !=  "None":
#            self.m_graph.addSeries(bjg)
#         if uwl !=  "None":
#            self.m_graph.addSeries(uwl)
#         if zdm !=  "None":
#            self.m_graph.addSeries(zdm)
#         if xtm !=  "None":
#            self.m_graph.addSeries(xtm)
#         if asn !=  "None":
#            self.m_graph.addSeries(asn)
#         if rzf !=  "None":
#            self.m_graph.addSeries(rzf)
#         if mzo !=  "None":
#            self.m_graph.addSeries(mzo)
#         if rqq !=  "None":
#            self.m_graph.addSeries(rqq)
#         if nbr !=  "None":
#            self.m_graph.addSeries(nbr)
#         if qxm !=  "None":
#            self.m_graph.addSeries(qxm)
#         if kdj !=  "None":
#            self.m_graph.addSeries(kdj)
#         if hrk !=  "None":
#            self.m_graph.addSeries(hrk)
#         if uhu !=  "None":
#            self.m_graph.addSeries(uhu)
#         if yge !=  "None":
#            self.m_graph.addSeries(yge)
#         if ovy !=  "None":
#            self.m_graph.addSeries(ovy)
#         if mlr !=  "None":
#            self.m_graph.addSeries(mlr)
#         if jjx !=  "None":
#            self.m_graph.addSeries(jjx)
#         if qol !=  "None":
#            self.m_graph.addSeries(qol)
#         if pgy !=  "None":
#            self.m_graph.addSeries(pgy)
#         if nej !=  "None":
#            self.m_graph.addSeries(nej)
#         if hbq !=  "None":
#            self.m_graph.addSeries(hbq)
#         if odw !=  "None":
#            self.m_graph.addSeries(odw)
#         if baw !=  "None":
#            self.m_graph.addSeries(baw)
#         if gzw !=  "None":
#            self.m_graph.addSeries(gzw)
#         if yaj !=  "None":
#            self.m_graph.addSeries(yaj)
#         if xja !=  "None":
#            self.m_graph.addSeries(xja)
#         if qni !=  "None":
#            self.m_graph.addSeries(qni)
#         if dbl !=  "None":
#            self.m_graph.addSeries(dbl)
#         if clr !=  "None":
#            self.m_graph.addSeries(clr)
#         if tyh !=  "None":
#            self.m_graph.addSeries(tyh)
#         if bah !=  "None":
#            self.m_graph.addSeries(bah)
#         if elg !=  "None":
#            self.m_graph.addSeries(elg)
#         if kda !=  "None":
#            self.m_graph.addSeries(kda)
#         if ync !=  "None":
#            self.m_graph.addSeries(ync)
#         if mzd !=  "None":
#            self.m_graph.addSeries(mzd)
#         if iku !=  "None":
#            self.m_graph.addSeries(iku)
#         if tau !=  "None":
#            self.m_graph.addSeries(tau)
#         if pzx !=  "None":
#            self.m_graph.addSeries(pzx)
#         if fsy !=  "None":
#            self.m_graph.addSeries(fsy)
#         if qmq !=  "None":
#            self.m_graph.addSeries(qmq)
#         if ugi !=  "None":
#            self.m_graph.addSeries(ugi)
#         if ods !=  "None":
#            self.m_graph.addSeries(ods)
#         if fjk !=  "None":
#            self.m_graph.addSeries(fjk)
#         if zfv !=  "None":
#            self.m_graph.addSeries(zfv)
#         if ecp !=  "None":
#            self.m_graph.addSeries(ecp)
#         if ukb !=  "None":
#            self.m_graph.addSeries(ukb)
#         if rhn !=  "None":
#            self.m_graph.addSeries(rhn)
#         if wgg !=  "None":
#            self.m_graph.addSeries(wgg)
#         if vbo !=  "None":
#            self.m_graph.addSeries(vbo)
#         if zws !=  "None":
#            self.m_graph.addSeries(zws)
#         if hpc !=  "None":
#            self.m_graph.addSeries(hpc)
#         if qdb !=  "None":
#            self.m_graph.addSeries(qdb)
#         if oaw !=  "None":
#            self.m_graph.addSeries(oaw)
#         if lcq !=  "None":
#            self.m_graph.addSeries(lcq)
#         if grc !=  "None":
#            self.m_graph.addSeries(grc)
#         if vkb !=  "None":
#            self.m_graph.addSeries(vkb)
#         if oyz !=  "None":
#            self.m_graph.addSeries(oyz)
#         if bzk !=  "None":
#            self.m_graph.addSeries(bzk)
#         if lyh !=  "None":
#            self.m_graph.addSeries(lyh)
#         if dfp !=  "None":
#            self.m_graph.addSeries(dfp)
#         if wru !=  "None":
#            self.m_graph.addSeries(wru)
#         if frg !=  "None":
#            self.m_graph.addSeries(frg)
#         if izu !=  "None":
#            self.m_graph.addSeries(izu)
#         if tqq !=  "None":
#            self.m_graph.addSeries(tqq)
#         if xlh !=  "None":
#            self.m_graph.addSeries(xlh)
#         if mes !=  "None":
#            self.m_graph.addSeries(mes)
#         if svf !=  "None":
#            self.m_graph.addSeries(svf)
#         if ipe !=  "None":
#            self.m_graph.addSeries(ipe)
#         if vyz !=  "None":
#            self.m_graph.addSeries(vyz)
#         if hgm !=  "None":
#            self.m_graph.addSeries(hgm)
#         if wyc !=  "None":
#            self.m_graph.addSeries(wyc)
#         if iwe !=  "None":
#            self.m_graph.addSeries(iwe)
#         if gow !=  "None":
#            self.m_graph.addSeries(gow)
#         if cem !=  "None":
#            self.m_graph.addSeries(cem)
#         if euv !=  "None":
#            self.m_graph.addSeries(euv)
#         if pmu !=  "None":
#            self.m_graph.addSeries(pmu)
#         if qfk !=  "None":
#            self.m_graph.addSeries(qfk)
#         if qmp !=  "None":
#            self.m_graph.addSeries(qmp)
#         if zpm !=  "None":
#            self.m_graph.addSeries(zpm)
#         if ily !=  "None":
#            self.m_graph.addSeries(ily)
#         if pbc !=  "None":
#            self.m_graph.addSeries(pbc)
#         if bhc !=  "None":
#            self.m_graph.addSeries(bhc)
#         if gwa !=  "None":
#            self.m_graph.addSeries(gwa)
#         if gbq !=  "None":
#            self.m_graph.addSeries(gbq)
#         if anq !=  "None":
#            self.m_graph.addSeries(anq)
#         if msq !=  "None":
#            self.m_graph.addSeries(msq)
#         if nkw !=  "None":
#            self.m_graph.addSeries(nkw)
#         if xfc !=  "None":
#            self.m_graph.addSeries(xfc)
#         if tmu !=  "None":
#            self.m_graph.addSeries(tmu)
#         if nqu !=  "None":
#            self.m_graph.addSeries(nqu)
#         if fkg !=  "None":
#            self.m_graph.addSeries(fkg)
#         if muv !=  "None":
#            self.m_graph.addSeries(muv)
#         if uja !=  "None":
#            self.m_graph.addSeries(uja)
#         if fjy !=  "None":
#            self.m_graph.addSeries(fjy)
#         if ppe !=  "None":
#            self.m_graph.addSeries(ppe)
#         if fpm !=  "None":
#            self.m_graph.addSeries(fpm)
#         if qob !=  "None":
#            self.m_graph.addSeries(qob)
#         if acw !=  "None":
#            self.m_graph.addSeries(acw)
#         if vyc !=  "None":
#            self.m_graph.addSeries(vyc)
#         if vzt !=  "None":
#            self.m_graph.addSeries(vzt)
#         if div !=  "None":
#            self.m_graph.addSeries(div)
#         if pcv !=  "None":
#            self.m_graph.addSeries(pcv)
#         if kmx !=  "None":
#            self.m_graph.addSeries(kmx)
#         if brn !=  "None":
#            self.m_graph.addSeries(brn)
#         if qgf !=  "None":
#            self.m_graph.addSeries(qgf)
#         if wzu !=  "None":
#            self.m_graph.addSeries(wzu)
#         if dkm !=  "None":
#            self.m_graph.addSeries(dkm)
#         if srf !=  "None":
#            self.m_graph.addSeries(srf)
#         if sdo !=  "None":
#            self.m_graph.addSeries(sdo)
#         if sby !=  "None":
#            self.m_graph.addSeries(sby)
#         if rjw !=  "None":
#            self.m_graph.addSeries(rjw)
#         if eln !=  "None":
#            self.m_graph.addSeries(eln)
#         if gxz !=  "None":
#            self.m_graph.addSeries(gxz)
#         if guq !=  "None":
#            self.m_graph.addSeries(guq)
#         if gsw !=  "None":
#            self.m_graph.addSeries(gsw)
#         if fsb !=  "None":
#            self.m_graph.addSeries(fsb)
#         if vtp !=  "None":
#            self.m_graph.addSeries(vtp)
#         if cxp !=  "None":
#            self.m_graph.addSeries(cxp)
#         if nea !=  "None":
#            self.m_graph.addSeries(nea)
#         if iaa !=  "None":
#            self.m_graph.addSeries(iaa)
#         if pez !=  "None":
#            self.m_graph.addSeries(pez)
#         if mdm !=  "None":
#            self.m_graph.addSeries(mdm)
#         if slf !=  "None":
#            self.m_graph.addSeries(slf)
#         if zfm !=  "None":
#            self.m_graph.addSeries(zfm)
#         if eak !=  "None":
#            self.m_graph.addSeries(eak)
#         if cdm !=  "None":
#            self.m_graph.addSeries(cdm)
#         if ymi !=  "None":
#            self.m_graph.addSeries(ymi)
#         if eax !=  "None":
#            self.m_graph.addSeries(eax)
#         if pfu !=  "None":
#            self.m_graph.addSeries(pfu)
#         if xui !=  "None":
#            self.m_graph.addSeries(xui)
#         if jrr !=  "None":
#            self.m_graph.addSeries(jrr)
#         if jiy !=  "None":
#            self.m_graph.addSeries(jiy)
#         if prv !=  "None":
#            self.m_graph.addSeries(prv)
#         if nml !=  "None":
#            self.m_graph.addSeries(nml)
#         if mxy !=  "None":
#            self.m_graph.addSeries(mxy)
#         if wto !=  "None":
#            self.m_graph.addSeries(wto)
#         if qoh !=  "None":
#            self.m_graph.addSeries(qoh)
#         if hvb !=  "None":
#            self.m_graph.addSeries(hvb)
#         if iqw !=  "None":
#            self.m_graph.addSeries(iqw)
#         if scj !=  "None":
#            self.m_graph.addSeries(scj)
#         if qhs !=  "None":
#            self.m_graph.addSeries(qhs)
#         if moj !=  "None":
#            self.m_graph.addSeries(moj)
#         if vtl !=  "None":
#            self.m_graph.addSeries(vtl)
#         if yxy !=  "None":
#            self.m_graph.addSeries(yxy)
#         if yak !=  "None":
#            self.m_graph.addSeries(yak)
#         if nta !=  "None":
#            self.m_graph.addSeries(nta)
#         if csv !=  "None":
#            self.m_graph.addSeries(csv)
#         if yrl !=  "None":
#            self.m_graph.addSeries(yrl)
#         if vxi !=  "None":
#            self.m_graph.addSeries(vxi)
#         if fuf !=  "None":
#            self.m_graph.addSeries(fuf)
#         if krz !=  "None":
#            self.m_graph.addSeries(krz)
#         if jvn !=  "None":
#            self.m_graph.addSeries(jvn)
#         if pnv !=  "None":
#            self.m_graph.addSeries(pnv)
#         if ezl !=  "None":
#            self.m_graph.addSeries(ezl)
#         if iau !=  "None":
#            self.m_graph.addSeries(iau)
#         if aaj !=  "None":
#            self.m_graph.addSeries(aaj)
#         if xir !=  "None":
#            self.m_graph.addSeries(xir)
#         if qdj !=  "None":
#            self.m_graph.addSeries(qdj)
#         if zel !=  "None":
#            self.m_graph.addSeries(zel)
#         if jej !=  "None":
#            self.m_graph.addSeries(jej)
#         if vds !=  "None":
#            self.m_graph.addSeries(vds)
#         if jxq !=  "None":
#            self.m_graph.addSeries(jxq)
#         if ras !=  "None":
#            self.m_graph.addSeries(ras)
#         if flw !=  "None":
#            self.m_graph.addSeries(flw)
#         if lfw !=  "None":
#            self.m_graph.addSeries(lfw)
#         if uoj !=  "None":
#            self.m_graph.addSeries(uoj)
#         if ohu !=  "None":
#            self.m_graph.addSeries(ohu)
#         if lxy !=  "None":
#            self.m_graph.addSeries(lxy)
#         if vyf !=  "None":
#            self.m_graph.addSeries(vyf)
#         if znr !=  "None":
#            self.m_graph.addSeries(znr)
#         if sox !=  "None":
#            self.m_graph.addSeries(sox)
#         if ukw !=  "None":
#            self.m_graph.addSeries(ukw)
#         if meh !=  "None":
#            self.m_graph.addSeries(meh)
#         if qmm !=  "None":
#            self.m_graph.addSeries(qmm)
#         if yef !=  "None":
#            self.m_graph.addSeries(yef)
#         if zkn !=  "None":
#            self.m_graph.addSeries(zkn)
#         if het !=  "None":
#            self.m_graph.addSeries(het)
#         if zai !=  "None":
#            self.m_graph.addSeries(zai)
#         if tmq !=  "None":
#            self.m_graph.addSeries(tmq)
#         if qyn !=  "None":
#            self.m_graph.addSeries(qyn)
#         if mws !=  "None":
#            self.m_graph.addSeries(mws)
#         if rwb !=  "None":
#            self.m_graph.addSeries(rwb)
#         if aok !=  "None":
#            self.m_graph.addSeries(aok)
#         if efp !=  "None":
#            self.m_graph.addSeries(efp)
#         if qqi !=  "None":
#            self.m_graph.addSeries(qqi)
#         if qit !=  "None":
#            self.m_graph.addSeries(qit)
#         if tfx !=  "None":
#            self.m_graph.addSeries(tfx)
#         if wxp !=  "None":
#            self.m_graph.addSeries(wxp)
#         if fjo !=  "None":
#            self.m_graph.addSeries(fjo)
#         if gtf !=  "None":
#            self.m_graph.addSeries(gtf)
#         if juo !=  "None":
#            self.m_graph.addSeries(juo)
#         if bsh !=  "None":
#            self.m_graph.addSeries(bsh)
#         if gvt !=  "None":
#            self.m_graph.addSeries(gvt)
#         if cln !=  "None":
#            self.m_graph.addSeries(cln)
#         if rzk !=  "None":
#            self.m_graph.addSeries(rzk)
#         if jsk !=  "None":
#            self.m_graph.addSeries(jsk)
#         if zyv !=  "None":
#            self.m_graph.addSeries(zyv)
#         if phn !=  "None":
#            self.m_graph.addSeries(phn)
#         if pco !=  "None":
#            self.m_graph.addSeries(pco)
#         if gsi !=  "None":
#            self.m_graph.addSeries(gsi)
#         if jri !=  "None":
#            self.m_graph.addSeries(jri)
#         if tqs !=  "None":
#            self.m_graph.addSeries(tqs)
#         if mfh !=  "None":
#            self.m_graph.addSeries(mfh)
#         if yfm !=  "None":
#            self.m_graph.addSeries(yfm)
#         if cdi !=  "None":
#            self.m_graph.addSeries(cdi)
#         if zay !=  "None":
#            self.m_graph.addSeries(zay)
#         if ecs !=  "None":
#            self.m_graph.addSeries(ecs)
#         if txv !=  "None":
#            self.m_graph.addSeries(txv)
#         if ant !=  "None":
#            self.m_graph.addSeries(ant)
#         if ay !=  "None":
#            self.m_graph.addSeries(ay)
#         if aul !=  "None":
#            self.m_graph.addSeries(aul)
#         if kwr !=  "None":
#            self.m_graph.addSeries(kwr)
#         if zqb !=  "None":
#            self.m_graph.addSeries(zqb)
#         if wqv !=  "None":
#            self.m_graph.addSeries(wqv)
#         if jtz !=  "None":
#            self.m_graph.addSeries(jtz)
#         if cds !=  "None":
#            self.m_graph.addSeries(cds)
#         if luj !=  "None":
#            self.m_graph.addSeries(luj)
#         if gal !=  "None":
#            self.m_graph.addSeries(gal)
#         if hyf !=  "None":
#            self.m_graph.addSeries(hyf)
#         if jmi !=  "None":
#            self.m_graph.addSeries(jmi)
#         if npr !=  "None":
#            self.m_graph.addSeries(npr)
#         if dwy !=  "None":
#            self.m_graph.addSeries(dwy)
#         if ehs !=  "None":
#            self.m_graph.addSeries(ehs)
#         if hfq !=  "None":
#            self.m_graph.addSeries(hfq)
#         if zcw !=  "None":
#            self.m_graph.addSeries(zcw)
#         if qnu !=  "None":
#            self.m_graph.addSeries(qnu)
#         if aer !=  "None":
#            self.m_graph.addSeries(aer)
#         if pej !=  "None":
#            self.m_graph.addSeries(pej)
#         if fru !=  "None":
#            self.m_graph.addSeries(fru)
#         if mub !=  "None":
#            self.m_graph.addSeries(mub)
#         if lkc !=  "None":
#            self.m_graph.addSeries(lkc)
#         if hjf !=  "None":
#            self.m_graph.addSeries(hjf)
#         if aab !=  "None":
#            self.m_graph.addSeries(aab)
#         if eqx !=  "None":
#            self.m_graph.addSeries(eqx)
#         if rtd !=  "None":
#            self.m_graph.addSeries(rtd)
#         if byn !=  "None":
#            self.m_graph.addSeries(byn)
#         if aoy !=  "None":
#            self.m_graph.addSeries(aoy)
#         if kat !=  "None":
#            self.m_graph.addSeries(kat)
#         if kru !=  "None":
#            self.m_graph.addSeries(kru)
#         if dkv !=  "None":
#            self.m_graph.addSeries(dkv)
#         if djw !=  "None":
#            self.m_graph.addSeries(djw)
#         if ezm !=  "None":
#            self.m_graph.addSeries(ezm)
#         if syb !=  "None":
#            self.m_graph.addSeries(syb)
#         if gbz !=  "None":
#            self.m_graph.addSeries(gbz)
#         if rhx !=  "None":
#            self.m_graph.addSeries(rhx)
#         if rge !=  "None":
#            self.m_graph.addSeries(rge)
#         if ise !=  "None":
#            self.m_graph.addSeries(ise)
#         if rev !=  "None":
#            self.m_graph.addSeries(rev)
#         if xwi !=  "None":
#            self.m_graph.addSeries(xwi)
#         if xti !=  "None":
#            self.m_graph.addSeries(xti)
#         if wxd !=  "None":
#            self.m_graph.addSeries(wxd)
#         if sli !=  "None":
#            self.m_graph.addSeries(sli)
#         if dek !=  "None":
#            self.m_graph.addSeries(dek)
#         if lgs !=  "None":
#            self.m_graph.addSeries(lgs)
#         if xkz !=  "None":
#            self.m_graph.addSeries(xkz)
#         if vpa !=  "None":
#            self.m_graph.addSeries(vpa)
#         if clv !=  "None":
#            self.m_graph.addSeries(clv)
#         if haf !=  "None":
#            self.m_graph.addSeries(haf)
#         if usu !=  "None":
#            self.m_graph.addSeries(usu)
#         if mmo !=  "None":
#            self.m_graph.addSeries(mmo)
#         if ntc !=  "None":
#            self.m_graph.addSeries(ntc)
#         if kay !=  "None":
#            self.m_graph.addSeries(kay)
#         if edr !=  "None":
#            self.m_graph.addSeries(edr)
#         if iiv !=  "None":
#            self.m_graph.addSeries(iiv)
#         if duj !=  "None":
#            self.m_graph.addSeries(duj)
#         if wtk !=  "None":
#            self.m_graph.addSeries(wtk)
#         if xdl !=  "None":
#            self.m_graph.addSeries(xdl)
#         if lwn !=  "None":
#            self.m_graph.addSeries(lwn)
#         if zrt !=  "None":
#            self.m_graph.addSeries(zrt)
#         if eol !=  "None":
#            self.m_graph.addSeries(eol)
#         if kgc !=  "None":
#            self.m_graph.addSeries(kgc)
#         if zks !=  "None":
#            self.m_graph.addSeries(zks)
#         if bad !=  "None":
#            self.m_graph.addSeries(bad)
#         if cyd !=  "None":
#            self.m_graph.addSeries(cyd)
#         if ach !=  "None":
#            self.m_graph.addSeries(ach)
#         if lox !=  "None":
#            self.m_graph.addSeries(lox)
#         if dsw !=  "None":
#            self.m_graph.addSeries(dsw)
#         if yuh !=  "None":
#            self.m_graph.addSeries(yuh)
#         if zgp !=  "None":
#            self.m_graph.addSeries(zgp)
#         if iib !=  "None":
#            self.m_graph.addSeries(iib)
#         if jkx !=  "None":
#            self.m_graph.addSeries(jkx)
#         if uwe !=  "None":
#            self.m_graph.addSeries(uwe)
#         if knh !=  "None":
#            self.m_graph.addSeries(knh)
#         if chk !=  "None":
#            self.m_graph.addSeries(chk)
#         if zgj !=  "None":
#            self.m_graph.addSeries(zgj)
#         if gka !=  "None":
#            self.m_graph.addSeries(gka)
#         if asa !=  "None":
#            self.m_graph.addSeries(asa)
#         if ioj !=  "None":
#            self.m_graph.addSeries(ioj)
#         if qak !=  "None":
#            self.m_graph.addSeries(qak)
#         if jov !=  "None":
#            self.m_graph.addSeries(jov)
#         if ynm !=  "None":
#            self.m_graph.addSeries(ynm)
#         if wdb !=  "None":
#            self.m_graph.addSeries(wdb)
#         if owe !=  "None":
#            self.m_graph.addSeries(owe)
#         if uod !=  "None":
#            self.m_graph.addSeries(uod)
#         if zjw !=  "None":
#            self.m_graph.addSeries(zjw)
#         if paj !=  "None":
#            self.m_graph.addSeries(paj)
#         if txi !=  "None":
#            self.m_graph.addSeries(txi)
#         if sab !=  "None":
#            self.m_graph.addSeries(sab)
#         if mhu !=  "None":
#            self.m_graph.addSeries(mhu)
#         if oyc !=  "None":
#            self.m_graph.addSeries(oyc)
#         if rtc !=  "None":
#            self.m_graph.addSeries(rtc)
#         if akf !=  "None":
#            self.m_graph.addSeries(akf)
#         if tzs !=  "None":
#            self.m_graph.addSeries(tzs)
#         if yba !=  "None":
#            self.m_graph.addSeries(yba)
#         if grp !=  "None":
#            self.m_graph.addSeries(grp)
#         if cdw !=  "None":
#            self.m_graph.addSeries(cdw)
#         if syx !=  "None":
#            self.m_graph.addSeries(syx)
#         if mnv !=  "None":
#            self.m_graph.addSeries(mnv)
#         if xeh !=  "None":
#            self.m_graph.addSeries(xeh)
#         if hxo !=  "None":
#            self.m_graph.addSeries(hxo)
#         if kkk !=  "None":
#            self.m_graph.addSeries(kkk)
#         if dwr !=  "None":
#            self.m_graph.addSeries(dwr)
#         if zpn !=  "None":
#            self.m_graph.addSeries(zpn)
#         if pnl !=  "None":
#            self.m_graph.addSeries(pnl)
#         if bgb !=  "None":
#            self.m_graph.addSeries(bgb)
#         if ivs !=  "None":
#            self.m_graph.addSeries(ivs)
#         if rcg !=  "None":
#            self.m_graph.addSeries(rcg)
#         if orn !=  "None":
#            self.m_graph.addSeries(orn)
#         if nwx !=  "None":
#            self.m_graph.addSeries(nwx)
#         if zrp !=  "None":
#            self.m_graph.addSeries(zrp)
#         if rmd !=  "None":
#            self.m_graph.addSeries(rmd)
#         if jnl !=  "None":
#            self.m_graph.addSeries(jnl)
#         if fvv !=  "None":
#            self.m_graph.addSeries(fvv)
#         if gyl !=  "None":
#            self.m_graph.addSeries(gyl)
#         if wgv !=  "None":
#            self.m_graph.addSeries(wgv)
#         if sqq !=  "None":
#            self.m_graph.addSeries(sqq)
#         if qzj !=  "None":
#            self.m_graph.addSeries(qzj)
#         if yve !=  "None":
#            self.m_graph.addSeries(yve)
#         if kos !=  "None":
#            self.m_graph.addSeries(kos)
#         if ece !=  "None":
#            self.m_graph.addSeries(ece)
#         if igk !=  "None":
#            self.m_graph.addSeries(igk)
#         if ybw !=  "None":
#            self.m_graph.addSeries(ybw)
#         if epa !=  "None":
#            self.m_graph.addSeries(epa)
#         if lsb !=  "None":
#            self.m_graph.addSeries(lsb)
#         if nvl !=  "None":
#            self.m_graph.addSeries(nvl)
#         if lem !=  "None":
#            self.m_graph.addSeries(lem)
#         if idi !=  "None":
#            self.m_graph.addSeries(idi)
#         if fzm !=  "None":
#            self.m_graph.addSeries(fzm)
#         if agm !=  "None":
#            self.m_graph.addSeries(agm)
#         if rja !=  "None":
#            self.m_graph.addSeries(rja)
#         if vfc !=  "None":
#            self.m_graph.addSeries(vfc)
#         if emy !=  "None":
#            self.m_graph.addSeries(emy)
#         if djk !=  "None":
#            self.m_graph.addSeries(djk)
#         if pw !=  "None":
#            self.m_graph.addSeries(pw)
#         if efq !=  "None":
#            self.m_graph.addSeries(efq)
#         if zpl !=  "None":
#            self.m_graph.addSeries(zpl)
#         if iks !=  "None":
#            self.m_graph.addSeries(iks)
#         if ypm !=  "None":
#            self.m_graph.addSeries(ypm)
#         if lme !=  "None":
#            self.m_graph.addSeries(lme)
#         if jba !=  "None":
#            self.m_graph.addSeries(jba)
#         if blt !=  "None":
#            self.m_graph.addSeries(blt)
#         if aod !=  "None":
#            self.m_graph.addSeries(aod)
#         if dkx !=  "None":
#            self.m_graph.addSeries(dkx)
#         if mey !=  "None":
#            self.m_graph.addSeries(mey)
#         if rdm !=  "None":
#            self.m_graph.addSeries(rdm)
#         if tlz !=  "None":
#            self.m_graph.addSeries(tlz)
#         if ivw !=  "None":
#            self.m_graph.addSeries(ivw)
#         if rpa !=  "None":
#            self.m_graph.addSeries(rpa)
#         if dgz !=  "None":
#            self.m_graph.addSeries(dgz)
#         if zpa !=  "None":
#            self.m_graph.addSeries(zpa)
#         if kto !=  "None":
#            self.m_graph.addSeries(kto)
#         if ltz !=  "None":
#            self.m_graph.addSeries(ltz)
#         if pfk !=  "None":
#            self.m_graph.addSeries(pfk)
#         if ema !=  "None":
#            self.m_graph.addSeries(ema)
#         if tjo !=  "None":
#            self.m_graph.addSeries(tjo)
#         if jje !=  "None":
#            self.m_graph.addSeries(jje)
#         if hzd !=  "None":
#            self.m_graph.addSeries(hzd)
#         if fxt !=  "None":
#            self.m_graph.addSeries(fxt)
#         if azp !=  "None":
#            self.m_graph.addSeries(azp)
#         if zmc !=  "None":
#            self.m_graph.addSeries(zmc)
#         if gxl !=  "None":
#            self.m_graph.addSeries(gxl)
#         if qiw !=  "None":
#            self.m_graph.addSeries(qiw)
#         if plt !=  "None":
#            self.m_graph.addSeries(plt)
#         if zhk !=  "None":
#            self.m_graph.addSeries(zhk)
#         if wpr !=  "None":
#            self.m_graph.addSeries(wpr)
#         if zrf !=  "None":
#            self.m_graph.addSeries(zrf)
#         if dwk !=  "None":
#            self.m_graph.addSeries(dwk)
#         if cwm !=  "None":
#            self.m_graph.addSeries(cwm)
#         if kyf !=  "None":
#            self.m_graph.addSeries(kyf)
#         if kfa !=  "None":
#            self.m_graph.addSeries(kfa)
#         if jnt !=  "None":
#            self.m_graph.addSeries(jnt)
#         if jjn !=  "None":
#            self.m_graph.addSeries(jjn)
#         if fii !=  "None":
#            self.m_graph.addSeries(fii)
#         if mjl !=  "None":
#            self.m_graph.addSeries(mjl)
#         if vdt !=  "None":
#            self.m_graph.addSeries(vdt)
#         if uga !=  "None":
#            self.m_graph.addSeries(uga)
#         if lff !=  "None":
#            self.m_graph.addSeries(lff)
#         if omm !=  "None":
#            self.m_graph.addSeries(omm)
#         if gyf !=  "None":
#            self.m_graph.addSeries(gyf)
#         if qhn !=  "None":
#            self.m_graph.addSeries(qhn)
#         if fpx !=  "None":
#            self.m_graph.addSeries(fpx)
#         if ksm !=  "None":
#            self.m_graph.addSeries(ksm)
#         if jyq !=  "None":
#            self.m_graph.addSeries(jyq)
#         if ilo !=  "None":
#            self.m_graph.addSeries(ilo)
#         if qbe !=  "None":
#            self.m_graph.addSeries(qbe)
#         if pxs !=  "None":
#            self.m_graph.addSeries(pxs)
#         if xup !=  "None":
#            self.m_graph.addSeries(xup)
#         if srs !=  "None":
#            self.m_graph.addSeries(srs)
#         if nzx !=  "None":
#            self.m_graph.addSeries(nzx)
#         if gda !=  "None":
#            self.m_graph.addSeries(gda)
#         if yxq !=  "None":
#            self.m_graph.addSeries(yxq)
#         if cuc !=  "None":
#            self.m_graph.addSeries(cuc)
#         if rrv !=  "None":
#            self.m_graph.addSeries(rrv)
#         if kem !=  "None":
#            self.m_graph.addSeries(kem)
#         if xbx !=  "None":
#            self.m_graph.addSeries(xbx)
#         if aug !=  "None":
#            self.m_graph.addSeries(aug)
#         if sjg !=  "None":
#            self.m_graph.addSeries(sjg)
#         if rjb !=  "None":
#            self.m_graph.addSeries(rjb)
#         if ipt !=  "None":
#            self.m_graph.addSeries(ipt)
#         if qhh !=  "None":
#            self.m_graph.addSeries(qhh)
#         if bpm !=  "None":
#            self.m_graph.addSeries(bpm)
#         if sma !=  "None":
#            self.m_graph.addSeries(sma)
#         if rex !=  "None":
#            self.m_graph.addSeries(rex)
#         if aql !=  "None":
#            self.m_graph.addSeries(aql)
#         if evp !=  "None":
#            self.m_graph.addSeries(evp)
#         if lxm !=  "None":
#            self.m_graph.addSeries(lxm)
#         if zop !=  "None":
#            self.m_graph.addSeries(zop)
#         if asm !=  "None":
#            self.m_graph.addSeries(asm)
#         if twg !=  "None":
#            self.m_graph.addSeries(twg)
#         if uak !=  "None":
#            self.m_graph.addSeries(uak)
#         if bwh !=  "None":
#            self.m_graph.addSeries(bwh)
#         if uke !=  "None":
#            self.m_graph.addSeries(uke)
#         if cpf !=  "None":
#            self.m_graph.addSeries(cpf)
#         if xcp !=  "None":
#            self.m_graph.addSeries(xcp)
#         if quv !=  "None":
#            self.m_graph.addSeries(quv)
#         if tnq !=  "None":
#            self.m_graph.addSeries(tnq)
#         if awu !=  "None":
#            self.m_graph.addSeries(awu)
#         if qud !=  "None":
#            self.m_graph.addSeries(qud)
#         if lvw !=  "None":
#            self.m_graph.addSeries(lvw)
#         if kuf !=  "None":
#            self.m_graph.addSeries(kuf)
#         if eph !=  "None":
#            self.m_graph.addSeries(eph)
#         if hxs !=  "None":
#            self.m_graph.addSeries(hxs)
#         if ifi !=  "None":
#            self.m_graph.addSeries(ifi)
#         if yag !=  "None":
#            self.m_graph.addSeries(yag)
#         if tbj !=  "None":
#            self.m_graph.addSeries(tbj)
#         if gah !=  "None":
#            self.m_graph.addSeries(gah)
#         if ybf !=  "None":
#            self.m_graph.addSeries(ybf)
#         if vnl !=  "None":
#            self.m_graph.addSeries(vnl)
#         if rgf !=  "None":
#            self.m_graph.addSeries(rgf)
#         if ezw !=  "None":
#            self.m_graph.addSeries(ezw)
#         if xul !=  "None":
#            self.m_graph.addSeries(xul)
#         if vqb !=  "None":
#            self.m_graph.addSeries(vqb)
#         if xlt !=  "None":
#            self.m_graph.addSeries(xlt)
#         if edi !=  "None":
#            self.m_graph.addSeries(edi)
#         if twn !=  "None":
#            self.m_graph.addSeries(twn)
#         if krk !=  "None":
#            self.m_graph.addSeries(krk)
#         if jcq !=  "None":
#            self.m_graph.addSeries(jcq)
#         if iez !=  "None":
#            self.m_graph.addSeries(iez)
#         if ady !=  "None":
#            self.m_graph.addSeries(ady)
#         if via !=  "None":
#            self.m_graph.addSeries(via)
#         if yiv !=  "None":
#            self.m_graph.addSeries(yiv)
#         if xyi !=  "None":
#            self.m_graph.addSeries(xyi)
#         if pif !=  "None":
#            self.m_graph.addSeries(pif)
#         if ket !=  "None":
#            self.m_graph.addSeries(ket)
#         if zzq !=  "None":
#            self.m_graph.addSeries(zzq)
#         if epi !=  "None":
#            self.m_graph.addSeries(epi)
#         if mxq !=  "None":
#            self.m_graph.addSeries(mxq)
#         if vby !=  "None":
#            self.m_graph.addSeries(vby)
#         if jpx !=  "None":
#            self.m_graph.addSeries(jpx)
#         if lru !=  "None":
#            self.m_graph.addSeries(lru)
#         if rae !=  "None":
#            self.m_graph.addSeries(rae)
#         if oiy !=  "None":
#            self.m_graph.addSeries(oiy)
#         if gam !=  "None":
#            self.m_graph.addSeries(gam)
#         if ljf !=  "None":
#            self.m_graph.addSeries(ljf)
#         if gha !=  "None":
#            self.m_graph.addSeries(gha)
#         if alb !=  "None":
#            self.m_graph.addSeries(alb)
#         if duq !=  "None":
#            self.m_graph.addSeries(duq)
#         if wyj !=  "None":
#            self.m_graph.addSeries(wyj)
#         if dck !=  "None":
#            self.m_graph.addSeries(dck)
#         if rwc !=  "None":
#            self.m_graph.addSeries(rwc)
#         if qlk !=  "None":
#            self.m_graph.addSeries(qlk)
#         if niy !=  "None":
#            self.m_graph.addSeries(niy)
#         if oxx !=  "None":
#            self.m_graph.addSeries(oxx)
#         if raz !=  "None":
#            self.m_graph.addSeries(raz)
#         if bjm !=  "None":
#            self.m_graph.addSeries(bjm)
#         if hmw !=  "None":
#            self.m_graph.addSeries(hmw)
#         if uae !=  "None":
#            self.m_graph.addSeries(uae)
#         if dnk !=  "None":
#            self.m_graph.addSeries(dnk)
#         if btz !=  "None":
#            self.m_graph.addSeries(btz)
#         if wgt !=  "None":
#            self.m_graph.addSeries(wgt)
#         if eoh !=  "None":
#            self.m_graph.addSeries(eoh)
#         if sgh !=  "None":
#            self.m_graph.addSeries(sgh)
#         if gri !=  "None":
#            self.m_graph.addSeries(gri)
#         if fgh !=  "None":
#            self.m_graph.addSeries(fgh)
#         if pvl !=  "None":
#            self.m_graph.addSeries(pvl)
#         if vhb !=  "None":
#            self.m_graph.addSeries(vhb)
#         if cfx !=  "None":
#            self.m_graph.addSeries(cfx)
#         if rkw !=  "None":
#            self.m_graph.addSeries(rkw)
#         if ezo !=  "None":
#            self.m_graph.addSeries(ezo)
#         if juu !=  "None":
#            self.m_graph.addSeries(juu)
#         if erc !=  "None":
#            self.m_graph.addSeries(erc)
#         if cyx !=  "None":
#            self.m_graph.addSeries(cyx)
#         if ewy !=  "None":
#            self.m_graph.addSeries(ewy)
#         if ylh !=  "None":
#            self.m_graph.addSeries(ylh)
#         if xwq !=  "None":
#            self.m_graph.addSeries(xwq)
#         if eri !=  "None":
#            self.m_graph.addSeries(eri)
#         if jsa !=  "None":
#            self.m_graph.addSeries(jsa)
#         if llk !=  "None":
#            self.m_graph.addSeries(llk)
#         if bec !=  "None":
#            self.m_graph.addSeries(bec)
#         if uhc !=  "None":
#            self.m_graph.addSeries(uhc)
#         if xhh !=  "None":
#            self.m_graph.addSeries(xhh)
#         if phf !=  "None":
#            self.m_graph.addSeries(phf)
#         if lvn !=  "None":
#            self.m_graph.addSeries(lvn)
#         if dca !=  "None":
#            self.m_graph.addSeries(dca)
#         if vfz !=  "None":
#            self.m_graph.addSeries(vfz)
#         if nvc !=  "None":
#            self.m_graph.addSeries(nvc)
#         if nsw !=  "None":
#            self.m_graph.addSeries(nsw)
#         if waj !=  "None":
#            self.m_graph.addSeries(waj)
#         if dqj !=  "None":
#            self.m_graph.addSeries(dqj)
#         if wnq !=  "None":
#            self.m_graph.addSeries(wnq)
#         if byw !=  "None":
#            self.m_graph.addSeries(byw)
#         if ypi !=  "None":
#            self.m_graph.addSeries(ypi)
#         if ygg !=  "None":
#            self.m_graph.addSeries(ygg)
#         if njn !=  "None":
#            self.m_graph.addSeries(njn)
#         if vxj !=  "None":
#            self.m_graph.addSeries(vxj)
#         if gvq !=  "None":
#            self.m_graph.addSeries(gvq)
#         if giv !=  "None":
#            self.m_graph.addSeries(giv)
#         if wpt !=  "None":
#            self.m_graph.addSeries(wpt)
#         if bog !=  "None":
#            self.m_graph.addSeries(bog)
#         if gzu !=  "None":
#            self.m_graph.addSeries(gzu)
#         if kcl !=  "None":
#            self.m_graph.addSeries(kcl)
#         if uco !=  "None":
#            self.m_graph.addSeries(uco)
#         if guz !=  "None":
#            self.m_graph.addSeries(guz)
#         if hby !=  "None":
#            self.m_graph.addSeries(hby)
#         if axj !=  "None":
#            self.m_graph.addSeries(axj)
#         if qve !=  "None":
#            self.m_graph.addSeries(qve)
#         if vov !=  "None":
#            self.m_graph.addSeries(vov)
#         if yfj !=  "None":
#            self.m_graph.addSeries(yfj)
#         if bph !=  "None":
#            self.m_graph.addSeries(bph)
#         if wad !=  "None":
#            self.m_graph.addSeries(wad)
#         if fpa !=  "None":
#            self.m_graph.addSeries(fpa)
#         if tnz !=  "None":
#            self.m_graph.addSeries(tnz)
#         if dbu !=  "None":
#            self.m_graph.addSeries(dbu)
#         if hyg !=  "None":
#            self.m_graph.addSeries(hyg)
#         if tav !=  "None":
#            self.m_graph.addSeries(tav)
#         if vyl !=  "None":
#            self.m_graph.addSeries(vyl)
#         if ovr !=  "None":
#            self.m_graph.addSeries(ovr)
#         if juj !=  "None":
#            self.m_graph.addSeries(juj)
#         if neb !=  "None":
#            self.m_graph.addSeries(neb)
#         if zwi !=  "None":
#            self.m_graph.addSeries(zwi)
#         if mio !=  "None":
#            self.m_graph.addSeries(mio)
#         if bhh !=  "None":
#            self.m_graph.addSeries(bhh)
#         if hqe !=  "None":
#            self.m_graph.addSeries(hqe)
#         if xga !=  "None":
#            self.m_graph.addSeries(xga)
#         if tnp !=  "None":
#            self.m_graph.addSeries(tnp)
#         if fmx !=  "None":
#            self.m_graph.addSeries(fmx)
#         if ewo !=  "None":
#            self.m_graph.addSeries(ewo)
#         if mlh !=  "None":
#            self.m_graph.addSeries(mlh)
#         if bqk !=  "None":
#            self.m_graph.addSeries(bqk)
#         if kcb !=  "None":
#            self.m_graph.addSeries(kcb)
#         if htt !=  "None":
#            self.m_graph.addSeries(htt)
#         if usp !=  "None":
#            self.m_graph.addSeries(usp)
#         if oil !=  "None":
#            self.m_graph.addSeries(oil)
#         if ttx !=  "None":
#            self.m_graph.addSeries(ttx)
#         if ajx !=  "None":
#            self.m_graph.addSeries(ajx)
#         if zac !=  "None":
#            self.m_graph.addSeries(zac)
#         if jll !=  "None":
#            self.m_graph.addSeries(jll)
#         if qrl !=  "None":
#            self.m_graph.addSeries(qrl)
#         if tkg !=  "None":
#            self.m_graph.addSeries(tkg)
#         if vrk !=  "None":
#            self.m_graph.addSeries(vrk)
#         if puu !=  "None":
#            self.m_graph.addSeries(puu)
#         if kpw !=  "None":
#            self.m_graph.addSeries(kpw)
#         if qop !=  "None":
#            self.m_graph.addSeries(qop)
#         if tkn !=  "None":
#            self.m_graph.addSeries(tkn)
#         if whe !=  "None":
#            self.m_graph.addSeries(whe)
#         if juh !=  "None":
#            self.m_graph.addSeries(juh)
#         if spn !=  "None":
#            self.m_graph.addSeries(spn)
#         if tcf !=  "None":
#            self.m_graph.addSeries(tcf)
#         if xxj !=  "None":
#            self.m_graph.addSeries(xxj)
#         if ogu !=  "None":
#            self.m_graph.addSeries(ogu)
#         if ywz !=  "None":
#            self.m_graph.addSeries(ywz)
#         if mwx !=  "None":
#            self.m_graph.addSeries(mwx)
#         if lvm !=  "None":
#            self.m_graph.addSeries(lvm)
#         if vzx !=  "None":
#            self.m_graph.addSeries(vzx)
#         if due !=  "None":
#            self.m_graph.addSeries(due)
#         if cxr !=  "None":
#            self.m_graph.addSeries(cxr)
#         if sug !=  "None":
#            self.m_graph.addSeries(sug)
#         if hhs !=  "None":
#            self.m_graph.addSeries(hhs)
#         if gbx !=  "None":
#            self.m_graph.addSeries(gbx)
#         if teu !=  "None":
#            self.m_graph.addSeries(teu)
#         if tur !=  "None":
#            self.m_graph.addSeries(tur)
#         if uju !=  "None":
#            self.m_graph.addSeries(uju)
#         if hhf !=  "None":
#            self.m_graph.addSeries(hhf)
#         if dma !=  "None":
#            self.m_graph.addSeries(dma)
#         if nsb !=  "None":
#            self.m_graph.addSeries(nsb)
#         if kdo !=  "None":
#            self.m_graph.addSeries(kdo)
#         if akr !=  "None":
#            self.m_graph.addSeries(akr)
#         if gqd !=  "None":
#            self.m_graph.addSeries(gqd)
#         if kkg !=  "None":
#            self.m_graph.addSeries(kkg)
#         if uit !=  "None":
#            self.m_graph.addSeries(uit)
#         if ibg !=  "None":
#            self.m_graph.addSeries(ibg)
#         if klu !=  "None":
#            self.m_graph.addSeries(klu)
#         if vbx !=  "None":
#            self.m_graph.addSeries(vbx)
#         if get !=  "None":
#            self.m_graph.addSeries(get)
#         if jqr !=  "None":
#            self.m_graph.addSeries(jqr)
#         if zuz !=  "None":
#            self.m_graph.addSeries(zuz)
#         if zkh !=  "None":
#            self.m_graph.addSeries(zkh)
#         if ppp !=  "None":
#            self.m_graph.addSeries(ppp)
#         if vtd !=  "None":
#            self.m_graph.addSeries(vtd)
#         if kzd !=  "None":
#            self.m_graph.addSeries(kzd)
#         if vhn !=  "None":
#            self.m_graph.addSeries(vhn)
#         if nuj !=  "None":
#            self.m_graph.addSeries(nuj)
#         if paq !=  "None":
#            self.m_graph.addSeries(paq)
#         if kwm !=  "None":
#            self.m_graph.addSeries(kwm)
#         if hyu !=  "None":
#            self.m_graph.addSeries(hyu)
#         if wae !=  "None":
#            self.m_graph.addSeries(wae)
#         if zom !=  "None":
#            self.m_graph.addSeries(zom)
#         if uth !=  "None":
#            self.m_graph.addSeries(uth)
#         if mnb !=  "None":
#            self.m_graph.addSeries(mnb)
#         if gfl !=  "None":
#            self.m_graph.addSeries(gfl)
#         if uck !=  "None":
#            self.m_graph.addSeries(uck)
#         if cwn !=  "None":
#            self.m_graph.addSeries(cwn)
#         if gjm !=  "None":
#            self.m_graph.addSeries(gjm)
#         if btk !=  "None":
#            self.m_graph.addSeries(btk)
#         if tlr !=  "None":
#            self.m_graph.addSeries(tlr)
#         if exb !=  "None":
#            self.m_graph.addSeries(exb)
#         if szr !=  "None":
#            self.m_graph.addSeries(szr)
#         if odt !=  "None":
#            self.m_graph.addSeries(odt)
#         if dwl !=  "None":
#            self.m_graph.addSeries(dwl)
#         if tez !=  "None":
#            self.m_graph.addSeries(tez)
#         if qgs !=  "None":
#            self.m_graph.addSeries(qgs)
#         if etb !=  "None":
#            self.m_graph.addSeries(etb)
#         if gqt !=  "None":
#            self.m_graph.addSeries(gqt)
#         if eqb !=  "None":
#            self.m_graph.addSeries(eqb)
#         if iyc !=  "None":
#            self.m_graph.addSeries(iyc)
#         if cux !=  "None":
#            self.m_graph.addSeries(cux)
#         if nlt !=  "None":
#            self.m_graph.addSeries(nlt)
#         if tcs !=  "None":
#            self.m_graph.addSeries(tcs)
#         if qdl !=  "None":
#            self.m_graph.addSeries(qdl)
#         if zea !=  "None":
#            self.m_graph.addSeries(zea)
#         if ufi !=  "None":
#            self.m_graph.addSeries(ufi)
#         if ugr !=  "None":
#            self.m_graph.addSeries(ugr)
#         if png !=  "None":
#            self.m_graph.addSeries(png)
#         if lbn !=  "None":
#            self.m_graph.addSeries(lbn)
#         if fye !=  "None":
#            self.m_graph.addSeries(fye)
#         if gpb !=  "None":
#            self.m_graph.addSeries(gpb)
#         if atk !=  "None":
#            self.m_graph.addSeries(atk)
#         if psz !=  "None":
#            self.m_graph.addSeries(psz)
#         if reg !=  "None":
#            self.m_graph.addSeries(reg)
#         if rzn !=  "None":
#            self.m_graph.addSeries(rzn)
#         if kiz !=  "None":
#            self.m_graph.addSeries(kiz)
#







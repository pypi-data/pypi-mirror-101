# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 18:14:29 2016

@author: becker
"""
import numpy as np
import scipy.linalg as linalg
import scipy.sparse as sparse
import simfempy.fems.bdrydata
from simfempy.fems import fem
from simfempy.tools import barycentric

#=================================================================#
class P1(fem.Fem):
    def __init__(self, mesh=None, dirichletmethod='trad'):
        super().__init__(mesh=mesh, dirichletmethod=dirichletmethod)
        self.dirichlet_al = 2
    def setMesh(self, mesh):
        super().setMesh(mesh)
        self.computeStencilCell(self.mesh.simplices)
        self.cellgrads = self.computeCellGrads()
    def nlocal(self): return self.mesh.dimension+1
    def nunknowns(self): return self.mesh.nnodes
    def dofspercell(self): return self.mesh.simplices
    def computeCellGrads(self):
        ncells, normals, cellsOfFaces, facesOfCells, dV = self.mesh.ncells, self.mesh.normals, self.mesh.cellsOfFaces, self.mesh.facesOfCells, self.mesh.dV
        scale = -1/self.mesh.dimension
        return scale*(normals[facesOfCells].T * self.mesh.sigma.T / dV.T).T
    def tonode(self, u): return u
    # strong bc
    def prepareBoundary(self, colorsdir, colorsflux=[]):
        bdrydata = simfempy.fems.bdrydata.BdryData()
        bdrydata.nodesdir={}
        # bdrydata.nodedirall = np.empty(shape=(0), dtype=np.int)
        bdrydata.nodedirall = np.empty(shape=(0), dtype=int)
        for color in colorsdir:
            facesdir = self.mesh.bdrylabels[color]
            bdrydata.nodesdir[color] = np.unique(self.mesh.faces[facesdir].flat[:])
            bdrydata.nodedirall = np.unique(np.union1d(bdrydata.nodedirall, bdrydata.nodesdir[color]))
        # print(f"{bdrydata.nodedirall=}")
        # bdrydata.nodesinner = np.setdiff1d(np.arange(self.mesh.nnodes, dtype=np.int),bdrydata.nodedirall)
        bdrydata.nodesinner = np.setdiff1d(np.arange(self.mesh.nnodes, dtype=int),bdrydata.nodedirall)
        bdrydata.nodesdirflux={}
        for color in colorsflux:
            facesdir = self.mesh.bdrylabels[color]
            bdrydata.nodesdirflux[color] = np.unique(self.mesh.faces[facesdir].ravel())
        return bdrydata
    def matrixBoundary(self, A, bdrydata):
        nodesdir, nodedirall, nodesinner, nodesdirflux = bdrydata.nodesdir, bdrydata.nodedirall, bdrydata.nodesinner, bdrydata.nodesdirflux
        nnodes = self.mesh.nnodes
        for color, nodes in nodesdirflux.items():
            nb = nodes.shape[0]
            help = sparse.dok_matrix((nb, nnodes))
            for i in range(nb): help[i, nodes[i]] = 1
            bdrydata.Asaved[color] = help.dot(A)
        bdrydata.A_inner_dir = A[nodesinner, :][:, nodedirall]
        if self.dirichletmethod == 'trad':
            help = np.ones((nnodes))
            help[nodedirall] = 0
            help = sparse.dia_matrix((help, 0), shape=(nnodes, nnodes))
            A = help.dot(A.dot(help))
            help = np.zeros((nnodes))
            help[nodedirall] = 1.0
            help = sparse.dia_matrix((help, 0), shape=(nnodes, nnodes))
            A += help
        else:
            bdrydata.A_dir_dir = self.dirichlet_al*A[nodedirall, :][:, nodedirall]
            help = np.ones(nnodes)
            help[nodedirall] = 0
            help = sparse.dia_matrix((help, 0), shape=(nnodes, nnodes))
            help2 = np.zeros(nnodes)
            help2[nodedirall] = np.sqrt(self.dirichlet_al)
            help2 = sparse.dia_matrix((help2, 0), shape=(nnodes, nnodes))
            A = help.dot(A.dot(help)) + help2.dot(A.dot(help2))
        return A, bdrydata
    def vectorBoundary(self, b, u, bdrycond, bdrydata):
        nodesdir, nodedirall, nodesinner, nodesdirflux = bdrydata.nodesdir, bdrydata.nodedirall, bdrydata.nodesinner, bdrydata.nodesdirflux
        if u is None: u = np.zeros_like(b)
        elif u.shape != b.shape : raise ValueError("u.shape != b.shape {} != {}".format(u.shape, b.shape))
        x, y, z = self.mesh.points.T
        for color, nodes in nodesdirflux.items():
            bdrydata.bsaved[color] = b[nodes]
        if self.dirichletmethod == 'trad':
            for color, nodes in nodesdir.items():
                if color in bdrycond.fct:
                    dirichlet = bdrycond.fct[color](x[nodes], y[nodes], z[nodes])
                    b[nodes] = dirichlet
                else:
                    b[nodes] = 0
                u[nodes] = b[nodes]
            b[nodesinner] -= bdrydata.A_inner_dir * b[nodedirall]
        else:
            for color, nodes in nodesdir.items():
                dirichlet = bdrycond.fct[color]
                if dirichlet:
                    u[nodes] = dirichlet(x[nodes], y[nodes], z[nodes])
                else:
                    u[nodes] = 0
                b[nodes] = 0
            b[nodesinner] -= bdrydata.A_inner_dir * u[nodedirall]
            b[nodedirall] += bdrydata.A_dir_dir * u[nodedirall]
        return b, u, bdrydata
    def vectorBoundaryZero(self, du, bdrydata):
        nodesdir = bdrydata.nodesdir
        for color, nodes in nodesdir.items():
            du[nodes] = 0
        return du
    # interpolate
    def interpolate(self, f):
        x, y, z = self.mesh.points.T
        return f(x, y, z)
    def interpolateBoundary(self, colors, f):
        """
        :param colors: set of colors to interpolate
        :param f: ditct of functions
        :return:
        """
        b = np.zeros(self.mesh.nnodes)
        for color in colors:
            if not color in f or not f[color]: continue
            faces = self.mesh.bdrylabels[color]
            normalsS = self.mesh.normals[faces]
            dS = linalg.norm(normalsS,axis=1)
            normalsS = normalsS/dS[:,np.newaxis]
            nx, ny, nz = normalsS.T
            nodes = np.unique(self.mesh.faces[faces].reshape(-1))
            x, y, z = self.mesh.points[nodes].T
            # constant normal !!
            nx, ny, nz = np.mean(normalsS, axis=0)
            try:
                b[nodes] = f[color](x, y, z, nx, ny, nz)
            except:
                b[nodes] = f[color](x, y, z)
        return b
    # matrices
    def computeMassMatrix(self, coeff=1):
        dimension, dV, nnodes = self.mesh.dimension, self.mesh.dV, self.mesh.nnodes
        massloc = barycentric.tensor(d=dimension, k=2)
        mass = np.einsum('n,kl->nkl', coeff*dV, massloc).ravel()
        return sparse.coo_matrix((mass, (self.rows, self.cols)), shape=(nnodes, nnodes)).tocsr()
    def computeBdryMassMatrix(self, colors=None, coeff=1, lumped=False):
        nnodes = self.mesh.nnodes
        rows = np.empty(shape=(0), dtype=int)
        cols = np.empty(shape=(0), dtype=int)
        mat = np.empty(shape=(0), dtype=float)
        if colors is None: colors = self.mesh.bdrylabels.keys()
        for color in colors:
            faces = self.mesh.bdrylabels[color]
            normalsS = self.mesh.normals[faces]
            if isinstance(coeff, dict):
                scalemass = coeff[color]
                dS = linalg.norm(normalsS, axis=1)
            else:
                scalemass = 1
                dS = linalg.norm(normalsS, axis=1)*coeff[faces]
            nodes = self.mesh.faces[faces]
            if lumped:
                scalemass /= self.mesh.dimension
                rows = np.append(rows, nodes)
                cols = np.append(cols, nodes)
                mass = np.repeat(scalemass * dS, self.mesh.dimension)
                mat = np.append(mat, mass)
            else:
                nloc = self.mesh.dimension
                rows = np.append(rows, np.repeat(nodes, nloc).reshape(-1))
                cols = np.append(cols, np.tile(nodes, nloc).reshape(-1))
                massloc = scalemass * simfempy.tools.barycentric.tensor(d=self.mesh.dimension-1, k=2)
                mat = np.append(mat, np.einsum('n,kl->nkl', dS, massloc).reshape(-1))
        return sparse.coo_matrix((mat, (rows, cols)), shape=(nnodes, nnodes)).tocsr()
    def computeMatrixTransport(self, lps):
        beta, betaC, ld = self.supdata['convection'], self.supdata['convectionC'], self.supdata['lam']
        nnodes, ncells, nfaces, dim = self.mesh.nnodes, self.mesh.ncells, self.mesh.nfaces, self.mesh.dimension
        if beta.shape != (nfaces,): raise TypeError(f"beta has wrong dimension {beta.shape=} expected {nfaces=}")
        if ld.shape != (ncells, dim+1): raise TypeError(f"ld has wrong dimension {ld.shape=}")
        mat = np.einsum('n,njk,nk,ni -> nij', self.mesh.dV, self.cellgrads[:,:,:dim], betaC, ld)
        A =  sparse.coo_matrix((mat.ravel(), (self.rows, self.cols)), shape=(nnodes, nnodes)).tocsr()
        if lps:
            A += self.computeMatrixLps(betaC)
        return A
    def computeMassMatrixSupg(self, xd, coeff=1):
        dim, dV, nnodes, xK = self.mesh.dimension, self.mesh.dV, self.mesh.nnodes, self.mesh.pointsc
        massloc = simfempy.tools.barycentric.tensor(d=dim, k=2)
        mass = np.einsum('n,ij->nij', coeff*dV, massloc)
        massloc = simfempy.tools.barycentric.tensor(d=dim, k=1)
        # marche si xd = xK + delta*betaC
        # mass += np.einsum('n,nik,nk,j -> nij', coeff*delta*dV, self.cellgrads[:,:,:dim], betaC, massloc)
        mass += np.einsum('n,nik,nk,j -> nij', coeff*dV, self.cellgrads[:,:,:dim], xd[:,:dim]-xK[:,:dim], massloc)
        return sparse.coo_matrix((mass.ravel(), (self.rows, self.cols)), shape=(nnodes, nnodes)).tocsr()
    # dotmat
    def formDiffusion(self, du, u, coeff):
        graduh = np.einsum('nij,ni->nj', self.cellgrads, u[self.mesh.simplices])
        graduh = np.einsum('ni,n->ni', graduh, self.mesh.dV*coeff)
        # du += np.einsum('nj,nij->ni', graduh, self.cellgrads)
        raise ValueError(f"graduh {graduh.shape} {du.shape}")
        return du
    def massDotCell(self, b, f, coeff=1):
        assert f.shape[0] == self.mesh.ncells
        dimension, simplices, dV = self.mesh.dimension, self.mesh.simplices, self.mesh.dV
        massloc = 1/(dimension+1)
        np.add.at(b, simplices, (massloc*coeff*dV*f)[:, np.newaxis])
        return b
    def massDot(self, b, f, coeff=1):
        dimension, simplices, dV = self.mesh.dimension, self.mesh.simplices, self.mesh.dV
        massloc = simfempy.tools.barycentric.tensor(d=dimension, k=2)
        r = np.einsum('n,kl,nl->nk', coeff*dV, massloc, f[simplices])
        np.add.at(b, simplices, r)
        return b
    def massDotSupg(self, b, f, coeff=1):
        xd = self.supdata['xd']
        dim, simp, points, dV, xK = self.mesh.dimension, self.mesh.simplices, self.mesh.points, self.mesh.dV, self.mesh.pointsc
        fm = f[simp].mean(axis=1)
        # marche si xd = xK + delta*betaC
        # r = np.einsum('n,nik,nk -> ni', delta*dV*fm, self.cellgrads[:,:,:dim], betaC)
        r = np.einsum('n,nik,nk -> ni', coeff*dV*fm, self.cellgrads[:,:,:dim], xd[:,:dim]-xK[:,:dim])
        # print(f"{r=}")
        np.add.at(b, simp, r)
        return b
    def massDotBoundary(self, b, f, colors=None, coeff=1, lumped=False):
        if colors is None: colors = self.mesh.bdrylabels.keys()
        for color in colors:
            faces = self.mesh.bdrylabels[color]
            normalsS = self.mesh.normals[faces]
            dS = linalg.norm(normalsS, axis=1)
            nodes = self.mesh.faces[faces]
            if isinstance(coeff, (int,float)): scalemass = coeff
            elif isinstance(coeff, dict): scalemass = coeff[color]
            else:
                assert coeff.shape[0]==self.mesh.nfaces
                scalemass = 1
                dS *= coeff[faces]
            # print(f"{scalemass=}")
            massloc = scalemass * simfempy.tools.barycentric.tensor(d=self.mesh.dimension-1, k=2)
            r = np.einsum('n,kl,nl->nk', dS, massloc, f[nodes])
            np.add.at(b, nodes, r)
        return b
    # rhs
    def computeRhsMass(self, b, rhs, mass):
        if rhs is None: return b
        x, y, z = self.mesh.points.T
        b += mass * rhs(x, y, z)
        return b
    def computeRhsCell(self, b, rhscell):
        if rhscell is None: return b
        scale = 1 / (self.mesh.dimension + 1)
        for label, fct in rhscell.items():
            if fct is None: continue
            cells = self.mesh.cellsoflabel[label]
            xc, yc, zc = self.mesh.pointsc[cells].T
            bC = scale * fct(xc, yc, zc) * self.mesh.dV[cells]
            # print("bC", bC)
            np.add.at(b, self.mesh.simplices[cells].T, bC)
        return b
    def computeRhsPoint(self, b, rhspoint):
        if rhspoint is None: return b
        for label, fct in rhspoint.items():
            if fct is None: continue
            points = self.mesh.verticesoflabel[label]
            xc, yc, zc = self.mesh.points[points].T
            # print("xc, yc, zc, f", xc, yc, zc, fct(xc, yc, zc))
            b[points] += fct(xc, yc, zc)
        return b
    def computeRhsBoundary(self, b, bdryfct, colors):
        normals =  self.mesh.normals
        scale = 1 / self.mesh.dimension
        for color in colors:
            faces = self.mesh.bdrylabels[color]
            if not color in bdryfct or bdryfct[color] is None: continue
            normalsS = normals[faces]
            dS = linalg.norm(normalsS,axis=1)
            normalsS = normalsS/dS[:,np.newaxis]
            assert(dS.shape[0] == len(faces))
            xf, yf, zf = self.mesh.pointsf[faces].T
            nx, ny, nz = normalsS.T
            bS = scale * bdryfct[color](xf, yf, zf, nx, ny, nz) * dS
            np.add.at(b, self.mesh.faces[faces].T, bS)
        return b
    def computeRhsBoundaryMass(self, b, bdrycond, types, mass):
        normals =  self.mesh.normals
        help = np.zeros(self.mesh.nnodes)
        for color, faces in self.mesh.bdrylabels.items():
            if bdrycond.type[color] not in types: continue
            if not color in bdrycond.fct or bdrycond.fct[color] is None: continue
            normalsS = normals[faces]
            dS = linalg.norm(normalsS,axis=1)
            normalsS = normalsS/dS[:,np.newaxis]
            nx, ny, nz = normalsS.T
            assert(dS.shape[0] == len(faces))
            nodes = np.unique(self.mesh.faces[faces].reshape(-1))
            x, y, z = self.mesh.points[nodes].T
            # constant normal !!
            nx, ny, nz = np.mean(normalsS, axis=0)
            help[nodes] = bdrycond.fct[color](x, y, z, nx, ny, nz)
        # print("help", help)
        b += mass*help
        return b
    # postprocess
    def computeErrorL2Cell(self, solexact, uh):
        xc, yc, zc = self.mesh.pointsc.T
        ec = solexact(xc, yc, zc) - np.mean(uh[self.mesh.simplices], axis=1)
        return np.sqrt(np.sum(ec**2* self.mesh.dV)), ec
    def computeErrorL2(self, solexact, uh):
        x, y, z = self.mesh.points.T
        en = solexact(x, y, z) - uh
        Men = np.zeros_like(en)
        return np.sqrt( np.dot(en, self.massDot(Men,en)) ), en
    def computeErrorFluxL2(self, solexact, diffcell, uh):
        xc, yc, zc = self.mesh.pointsc.T
        graduh = np.einsum('nij,ni->nj', self.cellgrads, uh[self.mesh.simplices])
        errv = 0
        for i in range(self.mesh.dimension):
            solxi = solexact.d(i, xc, yc, zc)
            errv += np.sum( diffcell*(solxi-graduh[:,i])**2* self.mesh.dV)
        return np.sqrt(errv)
    def computeBdryMean(self, u, colors):
        mean, omega = np.zeros(len(colors)), np.zeros(len(colors))
        for i,color in enumerate(colors):
            faces = self.mesh.bdrylabels[color]
            normalsS = self.mesh.normals[faces]
            dS = linalg.norm(normalsS, axis=1)
            omega[i] = np.sum(dS)
            mean[i] = np.sum(dS*np.mean(u[self.mesh.faces[faces]],axis=1))
        return mean/omega
    def comuteFluxOnRobin(self, u, faces, dS, uR, cR):
        uhmean =  np.sum(dS * np.mean(u[self.mesh.faces[faces]], axis=1))
        xf, yf, zf = self.mesh.pointsf[faces].T
        nx, ny, nz = np.mean(self.mesh.normals[faces], axis=0)
        if uR:
            try:
                uRmean =  np.sum(dS * uR(xf, yf, zf, nx, ny, nz))
            except:
                uRmean =  np.sum(dS * uR(xf, yf, zf))
        else: uRmean=0
        return cR*(uRmean-uhmean)
    def computeBdryNormalFlux(self, u, colors, bdrydata, bdrycond, diffcoff):
        flux, omega = np.zeros(len(colors)), np.zeros(len(colors))
        for i,color in enumerate(colors):
            faces = self.mesh.bdrylabels[color]
            normalsS = self.mesh.normals[faces]
            dS = linalg.norm(normalsS, axis=1)
            omega[i] = np.sum(dS)
            if color in bdrydata.bsaved.keys():
                bs, As = bdrydata.bsaved[color], bdrydata.Asaved[color]
                flux[i] = np.sum(As * u - bs)
            else:
                flux[i] = self.comuteFluxOnRobin(u, faces, dS, bdrycond.fct[color], bdrycond.param[color])
        return flux
    def computeBdryFct(self, u, colors):
        nodes = np.empty(shape=(0), dtype=int)
        for color in colors:
            faces = self.mesh.bdrylabels[color]
            nodes = np.unique(np.union1d(nodes, self.mesh.faces[faces].ravel()))
        return self.mesh.points[nodes], u[nodes]
    def computePointValues(self, u, colors):
        up = np.empty(len(colors))
        for i,color in enumerate(colors):
            nodes = self.mesh.verticesoflabel[color]
            up[i] = u[nodes]
        return up
    def computeMeanValues(self, u, colors):
        up = np.empty(len(colors))
        for i, color in enumerate(colors):
            up[i] = self.computeMeanValue(u,color)
        return up
    def computeMeanValue(self, u, color):
        cells = self.mesh.cellsoflabel[color]
        # print("umean", np.mean(u[self.mesh.simplices[cells]],axis=1))
        return np.sum(np.mean(u[self.mesh.simplices[cells]],axis=1)*self.mesh.dV[cells])

    #------------------------------
    def test(self):
        import scipy.sparse.linalg as splinalg
        colors = mesh.bdrylabels.keys()
        bdrydata = self.prepareBoundary(colorsdir=colors)
        A = self.computeMatrixDiffusion(coeff=1)
        A, bdrydata = self.matrixBoundary(A, bdrydata=bdrydata)
        b = np.zeros(self.nunknowns())
        rhs = np.vectorize(lambda x,y,z: 1)
        fp1 = self.interpolateCell(rhs)
        self.massDotCell(b, fp1, coeff=1)
        b = self.vectorBoundaryZero(b, bdrydata)
        return splinalg.spsolve(A, b)


# ------------------------------------- #

if __name__ == '__main__':
    from simfempy.meshes import testmeshes
    from simfempy.meshes import plotmesh
    import matplotlib.pyplot as plt

    mesh = testmeshes.backwardfacingstep(h=0.2)
    fem = P1(mesh)
    u = fem.test()
    plotmesh.meshWithBoundaries(mesh)
    plotmesh.meshWithData(mesh, point_data={'u':u}, title="P1 Test", alpha=1)
    plt.show()

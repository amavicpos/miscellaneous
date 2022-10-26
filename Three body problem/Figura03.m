%% Figure 03: Modified figure 02
%IS units unless otherwise stated
tic
clear all ; clc ;

%% Kepler-16 data (wiki)
AU=1.496E11 ; MS=1.988E30 ; day=86400 ;  % units, AU: Astronomica Unit
m1=0.6674*MS ; m2=m1 ; d=0.22*AU ; T=41.079*day ; % orbit % !!! Different d, T (with respect to figure 02)
r1=d*m2/(m1+m2) ; r2=d*m1/(m1+m2) ; % get stars positions
v1=2*pi*r1/T ; v2=2*pi*r2/T ; % get stars velocities
m3=m1 ; r3=0.7048*2*AU ; T3=228.776*2*day ; v3=2*pi*r3/T3 ; % planet % !!! Different m3

%% DEFINE BODIES
m=[m1 m2 m3]; % masses
r0=[[0.25*r1  0 0]' [-0.36*r2 0 0]' [-0.8*r3 0.1*r3 0]']; % initial r
v0=[[-0.02*v1 1.37*v1 0]' [-0.1*v2 -2.12*v2 0]' [0.12*v3 0.75*v3 0]']; % initial v

%%
tend=T3*0.551 ; % final time
NS=5E5 ; % number of steps
[vx,vy,vz,x,y,z,K,U,Ktot,Utot,E,Ltot,Lxtot,Lytot,Lztot,t]=VerletGravity(m,r0,v0,r3,tend,NS);

%% PLOTS
subplot(1,2,1) ; plot(x(1,:)/AU,y(1,:)/AU,x(2,:)/AU,y(2,:)/AU,x(3,:)/AU,y(3,:)/AU) ;
xlabel('Posición x (AU)'); ylabel('Posición y (AU)');
title('Trayectoria del sistema Kepler-16 modificado'); axis equal ; axis square ;
legend('Estrella Kepler-16A','Estrella Kepler-16A','Estrella Kepler-16A');
subplot(1,2,2) ; plot(t/day,Ktot,t/day,abs(Utot)); xlabel('Tiempo (días)');
ylabel('Energía (J)'); legend('Ktot','Utot (valor absoluto)'); title('Energías del sistema');
toc
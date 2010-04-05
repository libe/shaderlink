#include "filterwidth.h"
#include "filtered.h"
displacement displacement0()
{
// START NODE P0 

point P0_outPoint = P;
// END NODE P0 

// START NODE noiseF1 
float noiseF1_freq = 200.000;

float noiseF1_noise = noise(P0_outPoint * noiseF1_freq);
// END NODE noiseF1 

// START NODE multF0 
float multF0_inValue2 = 4.000;

float multF0_outValue = noiseF1_noise * multF0_inValue2;
// END NODE multF0 

// START NODE marble0 
color marble0_inColor1 = color(0.667,0.333,0.000);
color marble0_inColor2 = color(0.000,0.667,0.000);
float marble0_veining = 1.800;

#define snoise(x)    (noise(x) * 2 - 1)
#define MINFILTERWIDTH  1e-7
#define filterwidth_point(p) (max(sqrt(area(p)), MINFILTERWIDTH))
#define blend(a,b,x) ((a) * (1 - (x)) + (b) * (x))

color marble0_outColor;

color marble0_surfaceColor, marble0_layerColor;
color marble0_layerOpac;
point marble0_PP;
vector marble0_V;
normal marble0_Nf ;
float marble0_width, marble0_cutoff, marble0_fade, marble0_f, marble0_turb, marble0_maxfreq = 16;

/* init */
marble0_surfaceColor = 0;

marble0_Nf = faceforward(normalize(N), I);
marble0_V = -normalize(I);

/* compute turbulence */
marble0_PP = P0_outPoint * marble0_veining;

marble0_width = filterwidth_point(marble0_PP);
marble0_cutoff = clamp(0.5 / marble0_width, 0, marble0_maxfreq);

marble0_turb = 0;
for(marble0_f = 1; marble0_f < 0.5 * marble0_cutoff; marble0_f *= 2) 
    marble0_turb += abs(snoise(marble0_PP * marble0_f)) / marble0_f;
marble0_fade = clamp(2 * (marble0_cutoff - marble0_f) / marble0_cutoff, 0, 1);
marble0_turb += marble0_fade * abs(snoise(marble0_PP * marble0_f)) / marble0_f;

marble0_turb *= 0.5;  /* to match original rmarble turbulence value */

/* use turb to index into spline for layer color */

float marble0_r = comp(marble0_inColor1, 0);
float marble0_g = comp(marble0_inColor1, 1);
float marble0_b = comp(marble0_inColor1, 2);

marble0_layerColor = spline(marble0_turb,
        		       marble0_inColor1,
        		       marble0_inColor1,
        		       color(marble0_r, marble0_g+0.3, marble0_b+0.25),
        		       color(marble0_r-0.2, marble0_g+0.394, marble0_b+0.53),
        		       color(marble0_r-0.5, marble0_g+0.1, marble0_b+0.35),
        		       color(marble0_r-0.75, marble0_g+0.15, marble0_b+0.05),
        		       marble0_inColor2,
        		       marble0_inColor2); 
		       
marble0_layerOpac = 1;
marble0_surfaceColor = blend(marble0_surfaceColor, marble0_layerColor, marble0_layerOpac);

marble0_outColor = marble0_surfaceColor;
// END NODE marble0 

// START NODE colorToFloat0 

float colorToFloat0_outFloat = (comp(marble0_outColor, 0) + comp(marble0_outColor, 1) + comp(marble0_outColor, 2)) / 3;
// END NODE colorToFloat0 

// START NODE threshold0 
float threshold0_threshold = 0.360;
float threshold0_fuzz = 0.300;

float threshold0_outValue = smoothstep(threshold0_threshold,
												  threshold0_threshold + threshold0_fuzz, 
												  colorToFloat0_outFloat);
// END NODE threshold0 

// START NODE floatToColor0 

color floatToColor0_outColor = color(threshold0_outValue, threshold0_outValue, threshold0_outValue);
// END NODE floatToColor0 

// START NODE invertColor0 

color invertColor0_invertedColor = color(1 - comp(floatToColor0_outColor, 0),
												  1 - comp(floatToColor0_outColor, 1),
												  1 - comp(floatToColor0_outColor, 2));
// END NODE invertColor0 

// START NODE multFC0 
float multFC0_inValue1 = 0.400;

color multFC0_outValue = multFC0_inValue1 * invertColor0_invertedColor;
// END NODE multFC0 

// START NODE multFC1 

color multFC1_outValue = multF0_outValue * multFC0_outValue;
// END NODE multFC1 

// START NODE moon0 
float moon0_ka = 0.500;
float moon0_kd = 1.000;
float moon0_lacunarity = 1.500;
float moon0_octaves = 8.000;
float moon0_H = 0.300;
color moon0_highlandColor = color(0.700,0.700,0.700);
color moon0_mariaBaseColor = color(0.700,0.700,0.700);
color moon0_mariaColor = color(0.100,0.100,0.100);
float moon0_arg22 = 1.000;
float moon0_arg23 = 0.300;
float moon0_highlandThreshold = -0.200;
float moon0_highlandAltitude = 0.001;
float moon0_mariaAltitude = 0.001;
float moon0_peakRad = 0.007;
float moon0_innerRad = 0.010;
float moon0_rimRad = 0.020;
float moon0_outerRad = 0.050;
float moon0_peakHt = 0.005;
float moon0_rimHt = 0.003;
float moon0_numRays = 8.000;
float moon0_rayFade = 1.000;

#define snoise(Pt) (2*noise(Pt) - 1)
#define DNoise(p) (2*(point noise(p)) - point(1,1,1))
#define VLNoise(Pt,moon0_scale) (snoise(Pt + moon0_scale*DNoise(Pt)))
#define TWOPI (6.28)

float moon0_radialDist;
point moon0_PP, moon0_PQ;
float moon0_l, moon0_a, moon0_o, moon0_i, moon0_omega;
float moon0_chaos;
color moon0_outColor;
float moon0_temp1;
point moon0_vv;
float moon0_uu, moon0_ht, moon0_freq, moon0_scale;
float moon0_lighten;
point moon0_NN;
float moon0_pd;  /* pole distance */
float moon0_rayDist;

moon0_PQ = P;
moon0_PP = P0_outPoint;
moon0_NN = normalize(N);
moon0_radialDist = sqrt(xcomp(moon0_PP)*xcomp(moon0_PP) + ycomp(moon0_PP)*ycomp(moon0_PP));
moon0_omega = pow (moon0_lacunarity, (-.5)-moon0_H);

moon0_l = 1;  moon0_o = 1;  moon0_a = 0;
for(moon0_i = 0;  moon0_i < moon0_octaves;  moon0_i += 1)
{
    moon0_a += moon0_o * snoise(moon0_l * moon0_PP);
    moon0_l *= moon0_lacunarity;
    moon0_o *= moon0_omega;
}
moon0_chaos = moon0_a;

moon0_outColor = 1;

moon0_temp1 = moon0_radialDist * moon0_arg22;
if(moon0_temp1 < 1)
    moon0_chaos -= moon0_arg23 * (1 - smoothstep(0, 1, moon0_temp1));

if (moon0_chaos > moon0_highlandThreshold) {
    moon0_PQ += moon0_chaos * moon0_highlandAltitude * moon0_NN;
    moon0_outColor += moon0_highlandColor * moon0_chaos;
}
else {
    moon0_PQ += moon0_chaos * moon0_mariaAltitude * moon0_NN;
    moon0_outColor *= moon0_mariaBaseColor + moon0_mariaColor * moon0_chaos;
}

moon0_pd = 1-v;
moon0_vv = point(xcomp(moon0_PP)/moon0_radialDist, 0, zcomp(moon0_PP)/moon0_radialDist);
moon0_lighten = 0;
if (moon0_pd < moon0_peakRad) {
    moon0_uu = 1 - moon0_pd/moon0_peakRad;
    moon0_ht = moon0_peakHt * smoothstep(0, 1, moon0_uu);
}
else if (moon0_pd < moon0_innerRad) { 
    moon0_ht = 0;
}
else if (moon0_pd < moon0_rimRad) {           
    moon0_uu = (moon0_pd-moon0_innerRad) / (moon0_rimRad - moon0_innerRad);
    moon0_lighten = .75*moon0_uu;
    moon0_ht = moon0_rimHt * smoothstep(0, 1, moon0_uu);
}
else if (moon0_pd < moon0_outerRad) {        
    moon0_uu = 1 - (moon0_pd-moon0_rimRad) / (moon0_outerRad-moon0_rimRad);
    moon0_lighten = .75*moon0_uu*moon0_uu;
    moon0_ht = moon0_rimHt * smoothstep(0, 1, moon0_uu*moon0_uu);
}
else moon0_ht = 0;

moon0_PQ += moon0_ht * moon0_NN;
moon0_lighten *= 0.2;
moon0_outColor += color(moon0_lighten,moon0_lighten,moon0_lighten);

if (moon0_uu > 0) {
    if (moon0_pd < moon0_peakRad) {     
        moon0_vv = 5*moon0_PP + 3 * moon0_vv;
        moon0_freq = 1;  moon0_scale = 1;  moon0_ht = 0;
        for (moon0_i = 0;  moon0_i < 4;  moon0_i += 1) {
          moon0_ht += moon0_scale * snoise(moon0_freq * moon0_vv);
          moon0_freq *= 2;  moon0_scale *= 0.833;
        }

        moon0_PQ += 0.0025 * moon0_uu*moon0_ht * moon0_NN;
	}
    else {
        moon0_vv = 6*moon0_PP + 3 * moon0_vv;
        moon0_freq = 1;  moon0_scale = 1;  moon0_ht = 0;
        for(moon0_i = 0;  moon0_i < 4;  moon0_i += 1)
        {
            moon0_ht += moon0_scale * snoise(moon0_freq * moon0_vv);
            moon0_freq *= 2;  moon0_scale *= 0.833;
        }
        if(moon0_radialDist > moon0_rimRad)
            moon0_uu *= moon0_uu;
        moon0_PQ += 0.0025 * (0.5*moon0_uu + 0.5*moon0_ht) * moon0_NN;
	}
}

moon0_lighten = 0;
if (moon0_pd >= moon0_rimRad  &&  moon0_pd < 0.4) {
    moon0_lighten = smoothstep (.15, .5, snoise(62*u));
    moon0_rayDist = 0.2 + 0.2 * snoise (20 * mod(u+0.022,1));
    moon0_lighten *= (1 - smoothstep (moon0_rayDist-.2, moon0_rayDist, moon0_pd));
}
moon0_lighten = 0.2 * clamp (moon0_lighten, 0, 1);
moon0_outColor += color (moon0_lighten, moon0_lighten, moon0_lighten);
// END NODE moon0 

// START NODE colorToFloat1 

float colorToFloat1_outFloat = (comp(moon0_outColor, 0) + comp(moon0_outColor, 1) + comp(moon0_outColor, 2)) / 3;
// END NODE colorToFloat1 

// START NODE threshold1 
float threshold1_threshold = 0.650;
float threshold1_fuzz = 0.500;

float threshold1_outValue = smoothstep(threshold1_threshold,
												  threshold1_threshold + threshold1_fuzz, 
												  colorToFloat1_outFloat);
// END NODE threshold1 

// START NODE mixC0 
color mixC0_inColor2 = color(0.000,0.000,0.000);

color mixC0_outColor = mix((multFC1_outValue), (mixC0_inColor2), (threshold1_outValue));
// END NODE mixC0 

// START NODE sumFC0 

color sumFC0_outValue = mixC0_outColor + color(threshold1_outValue);
// END NODE sumFC0 

// START NODE colorToFloat2 

float colorToFloat2_outFloat = (comp(sumFC0_outValue, 0) + comp(sumFC0_outValue, 1) + comp(sumFC0_outValue, 2)) / 3;
// END NODE colorToFloat2 

// START NODE hump0 
float hump0_km = 0.016;

normal hump0_Ndiff = normalize(N) - normalize(Ng);
point hump0_outPoint = P - hump0_km * colorToFloat2_outFloat * normalize(N);
normal hump0_outNormal = calculatenormal(hump0_outPoint) + hump0_Ndiff;
// END NODE hump0 

// START NODE displacement0 

P = hump0_outPoint; N = hump0_outNormal;
// END NODE displacement0 

}

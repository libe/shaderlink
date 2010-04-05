/************************
 *
 * watermelon.sl
 * 
 * by Rudy Cortes - Copyright 2004(c)
 *************************/

#include "patterns.h"
#include "noises.h"

surface watermelon(
		   float Kd = 1;
           float Ks = 0.4;
           float roughness = 0.3;
           float Km = 0.0;
		   color baseColor= color (0.56,0.6,0.41);
		   float baseColorFreq = 4;
		   float label = 0.5;
		   color stripeColor = color(0.35,0.45,0.31);
		   float stripeFreq = 25;
		   float stripeNoiAmp = 0.015;
		   float stripeNoiLevels = 12;
		   float stripeNoiFreq = 5;
		   float detailFreq = 20;   
)
{
 /* Initialize shader variables */
  color sc,lc;
  float lo;

 /************************
  * 
  * Layer 1 - Base color 
  *
  ************************/

 /* Transform P from "current" to "shader" */
 point Pshad = transform("shader", P) * baseColorFreq + label;

 /*calculate a very simple noise to drive the spline function */
 float smallnoise = noise(2 * Pshad);

 /* create variations of the baseColor to pass it to the spline function*/
 color dargre = baseColor - 0.035;
 color midargre = baseColor - 0.0125;
 color midgre = baseColor;
 color midligre = baseColor + 0.02;
 color lightgre = baseColor + color (0.05,0.055,.01);

 /* use the spline function to color the base of the watermelon */
 sc = spline(smallnoise,dargre
	     ,midargre
	     ,midgre
	     ,midligre
	     ,midligre
	     ,midgre
	     ,midargre
	     ,midgre
	     ,midligre
	     ,lightgre);
 

 /******************************
  *
  * Layer 2 - Dark green stripes 
  *
  *******************************/

  /* compute base noise based on texture coords
   * This is a turbulence noise that uses gradual clamping
   * taken from Steve May's RmanNotes */

 float width = filterwidthp(Pshad);
 float cutoff = clamp(0.5 / width, 0, stripeNoiLevels); //4 = maxfreq
 float f;

 float turb =0;
 for (f = 1; f < 0.5 * cutoff; f *= 2) 
   turb += abs(snoise(Pshad * stripeNoiFreq * f)) / f;

 float fade = clamp(2 * (cutoff - f) / cutoff, 0, 1);
 turb += fade * abs(snoise(Pshad * f)) / f;

  /* perturb s based on turb, add the label to control randomness */
 float ss = s + snoise(turb + 912) * stripeNoiAmp + label;

  lc = stripeColor;
  /* use a noise to create broad long noisy stripes */
  float stripeOp = abs(snoisexy( stripeFreq * ss  , .6 * t ));
  lo = smoothpulse(.05,.3,.74,.94,stripeOp);    
  sc = mix(sc,lc,lo);
  

  /********
   *
   * Layer 3 - Veins  / Detail within the stripes 
   *
   *********/

 Pshad = label +  detailFreq * transform ("shader", P);
 float Pshadw = filterwidthp(Pshad);

 /*
  * First calculate the underlying color of the substrate
  * Use turbulence - use frequency clamping*/
 
 turb = 0.5 * turbulence (Pshad , Pshadw, 5, 2, 0.5);
   
  /* create variations of the stripeColor to pass it to the spline function*/
 dargre = stripeColor - 0.035;
 midargre = stripeColor - 0.0125;
 midgre = stripeColor;
 midligre = stripeColor + 0.02;
 lightgre = stripeColor + color (0.04,0.035,.01);  

 color stripeDetail = spline(turb,dargre
			     ,midargre
			     ,midgre
			     ,midligre
			     ,lightgre
			     ,midligre
			     ,midgre
			     ,lightgre
			     ,midargre
			     ,midgre
			     ,midligre
			     ,lightgre
			     ,midargre);

   float lo1 =  smoothpulse(.1, .3,.74,.94,stripeOp);				 

   sc = mix (sc,stripeDetail, lo1 *  smoothstep(0.1,.3,turb));


//  /* perturb the point lookup */
//   Pshad += vector(35.2,-21.9,6.25) + 0.5 * vfBm (Pshad, Pshadw, 6, 2, 0.5);

//   /* Now calculate the veining function for the lookup area */
//   float turbsum, freq, i;
//   turbsum = 0;  freq = 1;
//   Pshad *= .75; // scale down the scale of Pshad 
//   for (i = 0;  i < 4;  i += 1) {
//      turb = abs (filteredsnoise (Pshad * freq, Pshadw * freq)); 
//     turb = pow (smoothstep (0.55, .98, 1 - turb), 30) / freq;
//     turbsum += (1-turbsum) * turb;  
//     freq *= 2;
//    }
//   turbsum *= smoothstep (-0.1, 0.05, snoise((Pshad+vector(-4.4,8.34,27.1))));
  
//    sc = mix (sc, stripeColor * 0.9, turbsum * lo1);


  /* Layer 5 - Markings or spots */  
   
  /* Illumination model - Use regular plastic*/
    normal Nn = normalize(N);
    vector V = -normalize(I);
    //float Krr,Ktt;
    //fresnel(I,Nn,.25,Krr,Ktt);
    float bumpnoise = noise(Pshad * 0.45);

    Nn = normalize(calculatenormal(P + Nn*bumpnoise * Km));
    
 Oi = Os;
 Ci = Oi * sc * (diffuse(Nn) * Kd) + specular(Nn,V,roughness)*Ks ;
 //Ci = Oi * sc * (diffuse(Nn) * Kd);
 
}

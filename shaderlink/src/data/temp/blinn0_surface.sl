surface blinn0_surface()
{
// START NODE s0 

float s0_s = s;
// END NODE s0 

// START NODE t0 

float t0_t = t;
// END NODE t0 

// START NODE noiseST0 
float noiseST0_freq = 70.000;

float noiseST0_noise = noise(noiseST0_freq* s0_s, noiseST0_freq* t0_t);
// END NODE noiseST0 

// START NODE blinn0 
color blinn0_SurfaceColor = color(0.000,0.500,1.000);
color blinn0_ambientColor = color(0.000,0.000,0.000);
color blinn0_incandescence = color(0.000,0.000,0.000);
float blinn0_translucence = 0.000;
color blinn0_specularColor = color(0.500,0.500,0.500);
float blinn0_eccentricity = 0.300;
float blinn0_specularRollOff = 0.700;

 normal blinn0_Nf;
 vector blinn0_H, blinn0_Ln, blinn0_V;
 color blinn0_Ia, blinn0_Id, blinn0_Itr, blinn0_Is;
 float blinn0_NH, blinn0_NH2, blinn0_NHSQ, blinn0_Dd, blinn0_Gg, blinn0_VN, blinn0_VH, blinn0_LN, blinn0_Ff, blinn0_tmp;
 float blinn0_E= 1 / (blinn0_eccentricity * blinn0_eccentricity- 1);
  
 blinn0_Nf= faceforward(normalize(N), I);
 blinn0_Ia= ambient() + blinn0_ambientColor;
 blinn0_Id= noiseST0_noise* diffuse(blinn0_Nf);
 
 blinn0_Itr= 0;
 if (blinn0_translucence!= 0) {
  illuminance(P, blinn0_Nf, PI)
  blinn0_Itr+= Cl;
  blinn0_Itr*= blinn0_translucence;
 }
 
 blinn0_Is= 0;
 blinn0_V= normalize(-I);
 blinn0_VN= blinn0_V.blinn0_Nf;
 illuminance(P, blinn0_Nf, PI * 0.5) {
  blinn0_Ln= normalize(L);
  blinn0_H= normalize(blinn0_Ln+blinn0_V);
  blinn0_NH= blinn0_Nf.blinn0_H;
  blinn0_NHSQ= blinn0_NH*blinn0_NH;
  blinn0_NH2= blinn0_NH* 2;
  blinn0_Dd= (blinn0_E+1) / (blinn0_NHSQ+ blinn0_E);
  blinn0_Dd*= blinn0_Dd;
  blinn0_VH= blinn0_V.blinn0_H;
  blinn0_LN= blinn0_Ln.blinn0_Nf;
  if (blinn0_VN < blinn0_LN) {
   if (blinn0_VN* blinn0_NH2 < blinn0_VH)
   blinn0_Gg= blinn0_NH2/ blinn0_VH;
   else
   blinn0_Gg= 1 / blinn0_VN;
   }
  else {
   if (blinn0_LN* blinn0_NH2 < blinn0_VH)
   blinn0_Gg= (blinn0_LN* blinn0_NH2) / (blinn0_VH* blinn0_VN);
  else
  blinn0_Gg= 1 / blinn0_VN;
 }
 blinn0_tmp= pow((1 - blinn0_VH), 3);
 blinn0_Ff= blinn0_tmp+ (1 - blinn0_tmp) * blinn0_specularRollOff;
 blinn0_Is+= Cl * blinn0_Dd* blinn0_Gg* blinn0_Ff;
 }
 blinn0_Is*= blinn0_specularColor;
 
 color blinn0_outColor= blinn0_SurfaceColor* (blinn0_Ia + blinn0_Id + blinn0_Itr + blinn0_incandescence+ blinn0_Is);
// END NODE blinn0 

Ci = blinn0_outColor;}

#define DLLIMPORT extern "C" __declspec(dllimport)

#pragma comment(lib,"stagedll.lib")
#include <string>

//1[center], 2[left], 3[right]
DLLIMPORT int HomeSet(int iPos);				
DLLIMPORT int PABSet(int iPos, int ix, int iy);  //절대위치 
DLLIMPORT int SPDSet(int iPos,int ix, int iy);  // 드라이브 속도변경 
DLLIMPORT int POSRead(int iPos,int* ix, int* iy); //현재위치읽기 

DLLIMPORT int AutoOpenPort();
DLLIMPORT int PAB_POS(int iPos, int ix, int iy);

#define CENTER 1
#define LEFT 2
#define RIGHT 3

int main(int argc, char *argv[]){
	int rt_value = AutoOpenPort();

	if(0!=rt_value)
	{
		printf("AutoOpenPort Error");
		return 0;
	}
	
	int port_number = atoi(argv[1]);
	int param_ix = atoi(argv[2]);
	int param_iy = atoi(argv[3]);
	
	rt_value = SPDSet(port_number, 8000,8000);
	printf("%d:%d ", port_number, rt_value);
	if( rt_value != 0){
		printf("Speed Set Error");
		return 0;
	}
	
	rt_value = PAB_POS(port_number, param_ix, param_iy);
	printf("%d", rt_value);
	return rt_value;

	return 0;

}

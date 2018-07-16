#define DLLIMPORT extern "C" __declspec(dllimport)

#pragma comment(lib,"stagedll.lib")
#include <string>

//1[center], 2[left], 3[right]
DLLIMPORT int HomeSet(int iPos);
DLLIMPORT int PABSet(int iPos, int ix, int iy);  //절대위치 
DLLIMPORT int SPDSet(int iPos, int ix, int iy);  // 드라이브 속도변경 
DLLIMPORT int POSRead(int iPos, int* ix, int* iy); //현재위치읽기 

DLLIMPORT int AutoOpenPort();
DLLIMPORT int PAB_POS(int iPos, int ix, int iy);

#define CENTER 1
#define LEFT 2
#define RIGHT 3

int main(int argc, char *argv[]) {
	if (AutoOpenPort() != 0)
		printf("AutoOpenPort Error\n");

	int rt_value;
	for (int i = 1; i <= 3; i++) {
		rt_value = SPDSet(i, 8000, 8000);
		if (rt_value != 0) {
			printf("Speed set[%d] Error : %d\n", i, rt_value);
			return rt_value;
		}

		rt_value = HomeSet(i);
		if (rt_value != 0) {
			printf("Home set[%d] Error : %d\n", i, rt_value);
			return rt_value;
		}
	}
	printf("0");
	return 0;
}
